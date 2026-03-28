"""
Supabase database layer for D2C Voice-First Agent.

Provides persistent storage for:
- Orders
- Customers
- Conversations (message history)
- Support tickets
- Brands (Multi-tenant config)
- Products

Uses the official supabase-py client.
"""

import json
import uuid
from typing import Optional, List, Dict, Any

from supabase import create_client, Client
from logger import get_logger
from config import get_settings

settings = get_settings()

log = get_logger()

# We expect SUPABASE_URL and SUPABASE_SERVICE_KEY in settings or env
supabase_url = getattr(settings, "supabase_url", None)
supabase_key = getattr(settings, "supabase_service_key", None)

if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    log.warning("SUPABASE_URL or SUPABASE_SERVICE_KEY not set. Database operations will fail.")
    supabase = None


# ──────────────────────────────────────
# Product Catalog Queries
# ──────────────────────────────────────
def search_products(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Search for products matching a user's natural language query."""
    if not supabase:
        return []
    try:
        # Simple text search on name or description using Supabase textSearch
        response = supabase.table("products").select("*").text_search("name_desc_search", query).limit(limit).execute()
        
        # Fallback to ilike if text_search is not configured properly
        if not response.data:
            search_term = f"%{query}%"
            res1 = supabase.table("products").select("*").ilike("name", search_term).limit(limit).execute()
            res2 = supabase.table("products").select("*").ilike("description", search_term).limit(limit).execute()
            
            combined = {r["id"]: r for r in res1.data + res2.data}
            return list(combined.values())[:limit]
            
        return response.data
    except Exception as e:
        log.error(f"Error searching products: {e}")
        return []


# ──────────────────────────────────────
# Brand Queries
# ──────────────────────────────────────
def get_brand_by_phone(whatsapp_number: str) -> Optional[Dict[str, Any]]:
    """Get brand configuration by its WhatsApp number."""
    if not supabase:
        return None
    
    if whatsapp_number.startswith("whatsapp:"):
        whatsapp_number = whatsapp_number.replace("whatsapp:", "")
        
    try:
        response = supabase.table("brands").select("*").eq("whatsapp_number", whatsapp_number).execute()
        if response.data:
            return response.data[0]
            
        # Fallback for dev: return first brand
        fallback = supabase.table("brands").select("*").limit(1).execute()
        if fallback.data:
            return fallback.data[0]
            
    except Exception as e:
        log.error(f"Error getting brand by phone: {e}")
        
    return None


# ──────────────────────────────────────
# Order Queries
# ──────────────────────────────────────
def get_order_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    """Get the most recent order for a phone number."""
    if not supabase:
        return None
    
    if len(phone) == 10 and phone.isdigit():
        phone = f"+91{phone}"

    try:
        response = supabase.table("orders").select("*").eq("customer_phone", phone).order("created_at", desc=True).limit(1).execute()
        if response.data:
            return _format_order(response.data[0])
    except Exception as e:
        log.error(f"Error getting order by phone: {e}")
        
    return None


def get_order_by_id(order_id: str) -> Optional[Dict[str, Any]]:
    """Get an order by its order ID."""
    if not supabase:
        return None
    try:
        response = supabase.table("orders").select("*").eq("order_id", order_id).execute()
        if response.data:
            return _format_order(response.data[0])
    except Exception as e:
        log.error(f"Error getting order by id: {e}")
    return None


def process_refund(order_id: str) -> Dict[str, Any]:
    """Process a refund for an order."""
    if not supabase:
        return {"success": False, "message": "Supabase not configured."}
    
    order = get_order_by_id(order_id)
    if not order:
        return {"success": False, "message": "Order not found."}

    if order.get("status") not in ("Delivered", "Processing"):
        return {"success": False, "message": f"Cannot refund order in status: {order.get('status')}"}

    if order.get("refund_status"):
        return {"success": False, "message": f"Refund already in status: {order.get('refund_status')}"}

    try:
        supabase.table("orders").update({
            "refund_status": "Initiated"
        }).eq("order_id", order_id).execute()
        return {"success": True, "message": f"Refund initiated for order {order_id}"}
    except Exception as e:
        log.error(f"Error processing refund: {e}")
        return {"success": False, "message": str(e)}


def cancel_order(order_id: str) -> Dict[str, Any]:
    """Cancel an order (only if Processing)."""
    if not supabase:
        return {"success": False, "message": "Supabase not configured."}
    
    order = get_order_by_id(order_id)
    if not order:
        return {"success": False, "message": "Order not found."}

    if order.get("status") != "Processing":
        return {"success": False, "message": f"Cannot cancel order in status: {order.get('status')}"}

    try:
        supabase.table("orders").update({
            "status": "Cancelled",
            "refund_status": "Initiated"
        }).eq("order_id", order_id).execute()
        return {"success": True, "message": f"Order {order_id} cancelled and refund initiated."}
    except Exception as e:
        log.error(f"Error cancelling order: {e}")
        return {"success": False, "message": str(e)}


def _format_order(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure items are treated as JSON list and map phone."""
    try:
        if isinstance(order_data.get("items"), str):
            order_data["items"] = json.loads(order_data["items"])
    except json.JSONDecodeError:
        order_data["items"] = []
    
    order_data["phone"] = order_data.get("customer_phone", "")
    return order_data


# ──────────────────────────────────────
# Conversation Memory
# ──────────────────────────────────────
def save_message(phone: str, role: str, message: str, intent: str = "", lang: str = "en"):
    """Save a conversation message."""
    if not supabase:
        return
    try:
        supabase.table("conversations").insert({
            "phone": phone,
            "role": role,
            "message": message,
            "intent": intent,
            "detected_lang": lang
        }).execute()
    except Exception as e:
        log.error(f"Error saving message: {e}")


def get_conversation_history(phone: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent conversation history for a phone number."""
    if not supabase:
        return []
    try:
        response = supabase.table("conversations").select(
            "role, message, intent, detected_lang, created_at"
        ).eq("phone", phone).order("created_at", desc=False).limit(limit).execute()
        
        return response.data
    except Exception as e:
        log.error(f"Error getting history: {e}")
        return []


def get_conversation_summary(phone: str, limit: int = 5) -> str:
    """Get a formatted summary of recent conversation for LLM context."""
    history = get_conversation_history(phone, limit)
    if not history:
        return ""

    lines = []
    for msg in history:
        role = "Customer" if msg.get("role") == "user" else "Agent"
        lines.append(f"{role}: {msg.get('message')}")

    return "\n".join(lines)


# ──────────────────────────────────────
# Ticket System
# ──────────────────────────────────────
def create_ticket(phone: str, message: str, intent: str, image_url: Optional[str] = None) -> str:
    """Create a support ticket and return its ticket ID."""
    ticket_id = f"TKT-{str(uuid.uuid4()).split('-')[0].upper()}"

    if not supabase:
        return ticket_id
    
    try:
        supabase.table("tickets").insert({
            "ticket_id": ticket_id,
            "phone": phone,
            "message": message,
            "intent": intent,
            "image_url": image_url,
            "status": "open"
        }).execute()
        log.info(f"Support ticket created: {ticket_id} for {phone} (intent: {intent})")
    except Exception as e:
        log.error(f"Error creating ticket: {e}")
        
    return ticket_id


def get_open_tickets(phone: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get open tickets, optionally filtered by phone."""
    if not supabase:
        return []
    try:
        query = supabase.table("tickets").select("*").eq("status", "open")
        if phone:
            query = query.eq("phone", phone)
            
        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        log.error(f"Error getting open tickets: {e}")
        return []


def close_ticket(ticket_id: str) -> bool:
    """Close a support ticket."""
    if not supabase:
        return False
    try:
        response = supabase.table("tickets").update({
            "status": "closed"
        }).eq("ticket_id", ticket_id).execute()
        return len(response.data) > 0
    except Exception as e:
        log.error(f"Error closing ticket: {e}")
        return False
