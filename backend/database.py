"""
SQLite database layer for D2C Voice-First Agent.

Provides persistent storage for:
- Orders (replacing the mock in-memory dict)
- Customers
- Conversations (message history)
- Support tickets

Uses SQLite for local dev / single-server; swap the connection string
for PostgreSQL/Supabase in production.
"""

import sqlite3
import json
from typing import Optional
from contextlib import contextmanager

from logger import get_logger
from config import get_settings

DB_PATH = get_settings().database_path

log = get_logger()


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create all tables if they don't exist and seed sample data."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                whatsapp_number TEXT UNIQUE NOT NULL,
                custom_prompt TEXT DEFAULT '',
                webhook_url TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                name TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE NOT NULL,
                customer_phone TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Processing',
                items TEXT NOT NULL DEFAULT '[]',
                estimated_delivery TEXT DEFAULT '',
                refund_status TEXT DEFAULT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (customer_phone) REFERENCES customers(phone)
            );

            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                message TEXT NOT NULL,
                intent TEXT DEFAULT '',
                detected_lang TEXT DEFAULT 'en',
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                message TEXT NOT NULL,
                intent TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'open',
                assigned_to TEXT DEFAULT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_orders_phone ON orders(customer_phone);
            CREATE INDEX IF NOT EXISTS idx_orders_order_id ON orders(order_id);
            CREATE INDEX IF NOT EXISTS idx_conversations_phone ON conversations(phone);
            CREATE INDEX IF NOT EXISTS idx_tickets_phone ON tickets(phone);
            CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
        """)

        # Seed sample brand if brands table is empty
        cursor = conn.execute("SELECT COUNT(*) FROM brands")
        if cursor.fetchone()[0] == 0:
            conn.execute(
                "INSERT INTO brands (name, whatsapp_number, custom_prompt, webhook_url) VALUES (?, ?, ?, ?)",
                ("Acme D2C", "+14155238886", "You are a highly professional and polite support agent for Acme D2C. Be concise and empathetic.", "http://localhost:8000/api/v1/dummy_webhook_receiver")
            )

        # Seed sample data if orders table is empty
        cursor = conn.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] == 0:
            _seed_sample_data(conn)

    log.info("Database initialized successfully")


def _seed_sample_data(conn: sqlite3.Connection):
    """Insert sample customers and orders for demo/dev."""
    customers = [
        ("+919876543210", "Rahul Sharma"),
        ("+919988776655", "Priya Patel"),
        ("+918877665544", "Amit Kumar"),
        ("+917766554433", "Sneha Gupta"),
    ]
    for phone, name in customers:
        conn.execute(
            "INSERT OR IGNORE INTO customers (phone, name) VALUES (?, ?)",
            (phone, name),
        )

    orders = [
        ("ORD-12345", "+919876543210", "Out for Delivery", '["Wireless Earbuds", "Phone Case"]', "Today by 8 PM", None),
        ("ORD-67890", "+919988776655", "Delivered", '["Smart Watch"]', "Delivered on 5th Oct", "Processing"),
        ("ORD-11223", "+918877665544", "Processing", '["Running Shoes"]', "10th Oct", None),
        ("ORD-44556", "+917766554433", "Cancelled", '["Yoga Mat"]', "N/A", "Refunded"),
    ]
    for order_id, phone, status, items, delivery, refund in orders:
        conn.execute(
            "INSERT OR IGNORE INTO orders (order_id, customer_phone, status, items, estimated_delivery, refund_status) VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, phone, status, items, delivery, refund),
        )

    log.info("Seeded sample data: 4 customers, 4 orders")


# ──────────────────────────────────────
# Brand Queries
# ──────────────────────────────────────
def get_brand_by_phone(whatsapp_number: str) -> Optional[dict]:
    """Get brand configuration by its WhatsApp number."""
    # Twilio sandbox numbers sometimes have formats like whatsapp:+14155238886
    if whatsapp_number.startswith("whatsapp:"):
        whatsapp_number = whatsapp_number.replace("whatsapp:", "")
        
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM brands WHERE whatsapp_number = ?",
            (whatsapp_number,)
        ).fetchone()
        if row:
            return dict(row)
        
        # Fallback to the first brand if using an unmapped number (for dev)
        row = conn.execute("SELECT * FROM brands LIMIT 1").fetchone()
        if row:
            return dict(row)
    return None


# ──────────────────────────────────────
# Order Queries
# ──────────────────────────────────────
def get_order_by_phone(phone: str) -> Optional[dict]:
    """Get the most recent order for a phone number."""
    if len(phone) == 10 and phone.isdigit():
        phone = f"+91{phone}"

    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM orders WHERE customer_phone = ? ORDER BY created_at DESC LIMIT 1",
            (phone,),
        ).fetchone()
        if row:
            return _row_to_order(row)
    return None


def get_order_by_id(order_id: str) -> Optional[dict]:
    """Get an order by its order ID."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM orders WHERE order_id = ?", (order_id,)
        ).fetchone()
        if row:
            return _row_to_order(row)
    return None


def process_refund(order_id: str) -> dict:
    """Process a refund for an order."""
    order = get_order_by_id(order_id)
    if not order:
        return {"success": False, "message": "Order not found."}

    if order["status"] not in ("Delivered", "Processing"):
        return {"success": False, "message": f"Cannot refund order in status: {order['status']}"}

    if order["refund_status"]:
        return {"success": False, "message": f"Refund already in status: {order['refund_status']}"}

    with get_db() as conn:
        conn.execute(
            "UPDATE orders SET refund_status = 'Initiated', updated_at = datetime('now') WHERE order_id = ?",
            (order_id,),
        )
    return {"success": True, "message": f"Refund initiated for order {order_id}"}


def cancel_order(order_id: str) -> dict:
    """Cancel an order (only if Processing)."""
    order = get_order_by_id(order_id)
    if not order:
        return {"success": False, "message": "Order not found."}

    if order["status"] != "Processing":
        return {"success": False, "message": f"Cannot cancel order in status: {order['status']}"}

    with get_db() as conn:
        conn.execute(
            "UPDATE orders SET status = 'Cancelled', refund_status = 'Initiated', updated_at = datetime('now') WHERE order_id = ?",
            (order_id,),
        )
    return {"success": True, "message": f"Order {order_id} cancelled and refund initiated."}


def _row_to_order(row: sqlite3.Row) -> dict:
    """Convert a database row to an order dict."""
    d = dict(row)
    d["items"] = json.loads(d.get("items", "[]"))
    d["phone"] = d.get("customer_phone", "")
    return d


# ──────────────────────────────────────
# Conversation Memory
# ──────────────────────────────────────
def save_message(phone: str, role: str, message: str, intent: str = "", lang: str = "en"):
    """Save a conversation message."""
    with get_db() as conn:
        conn.execute(
            "INSERT INTO conversations (phone, role, message, intent, detected_lang) VALUES (?, ?, ?, ?, ?)",
            (phone, role, message, intent, lang),
        )


def get_conversation_history(phone: str, limit: int = 10) -> list[dict]:
    """Get recent conversation history for a phone number."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT role, message, intent, detected_lang, created_at FROM conversations WHERE phone = ? ORDER BY created_at DESC LIMIT ?",
            (phone, limit),
        ).fetchall()
        # Return in chronological order
        return [dict(r) for r in reversed(rows)]


def get_conversation_summary(phone: str, limit: int = 5) -> str:
    """Get a formatted summary of recent conversation for LLM context."""
    history = get_conversation_history(phone, limit)
    if not history:
        return ""

    lines = []
    for msg in history:
        role = "Customer" if msg["role"] == "user" else "Agent"
        lines.append(f"{role}: {msg['message']}")

    return "\n".join(lines)


# ──────────────────────────────────────
# Ticket System
# ──────────────────────────────────────
def create_ticket(phone: str, message: str, intent: str) -> str:
    """Create a support ticket and return its ticket ID."""
    import uuid
    ticket_id = f"TKT-{str(uuid.uuid4()).split('-')[0].upper()}"

    with get_db() as conn:
        conn.execute(
            "INSERT INTO tickets (ticket_id, phone, message, intent) VALUES (?, ?, ?, ?)",
            (ticket_id, phone, message, intent),
        )

    log.info(f"Support ticket created: {ticket_id} for {phone} (intent: {intent})")
    return ticket_id


def get_open_tickets(phone: str | None = None) -> list[dict]:
    """Get open tickets, optionally filtered by phone."""
    with get_db() as conn:
        if phone:
            rows = conn.execute(
                "SELECT * FROM tickets WHERE phone = ? AND status = 'open' ORDER BY created_at DESC",
                (phone,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tickets WHERE status = 'open' ORDER BY created_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]


def close_ticket(ticket_id: str) -> bool:
    """Close a support ticket."""
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE tickets SET status = 'closed', updated_at = datetime('now') WHERE ticket_id = ?",
            (ticket_id,),
        )
        return cursor.rowcount > 0
