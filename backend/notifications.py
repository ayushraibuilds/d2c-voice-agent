"""
Proactive Notifications for D2C Voice-First Agent.

Handles outbound messages for:
  - Shipping updates
  - Delivery confirmations
  - CSAT (Customer Satisfaction) collection
  - Order status changes

Uses Twilio's WhatsApp Business API for delivery.
"""

from datetime import datetime
from logger import get_logger
import database as db

log = get_logger()


# ──────────────────────────────────────
# CSAT Collection
# ──────────────────────────────────────
CSAT_PENDING: dict[str, str] = {}  # phone → ticket_id awaiting rating


def request_csat(phone: str, ticket_id: str) -> str:
    """
    Generate a CSAT request message and mark as pending.
    Returns the message text to send.
    """
    CSAT_PENDING[phone] = ticket_id
    return (
        "🌟 Your issue has been resolved! How was your experience?\n\n"
        "Reply with a number:\n"
        "1 ⭐ — Very Poor\n"
        "2 ⭐⭐ — Poor\n"
        "3 ⭐⭐⭐ — Average\n"
        "4 ⭐⭐⭐⭐ — Good\n"
        "5 ⭐⭐⭐⭐⭐ — Excellent"
    )


def is_csat_response(phone: str, message: str) -> bool:
    """Check if a message is a CSAT rating response."""
    return phone in CSAT_PENDING and message.strip() in ("1", "2", "3", "4", "5")


def process_csat_response(phone: str, message: str) -> str:
    """Process a CSAT rating and store it."""
    rating = int(message.strip())
    ticket_id = CSAT_PENDING.pop(phone, "")

    # Store CSAT in the tickets table as a note
    if ticket_id:
        with db.get_db() as conn:
            conn.execute(
                "UPDATE tickets SET status = 'closed', updated_at = datetime('now') WHERE ticket_id = ?",
                (ticket_id,),
            )
        log.info(f"CSAT recorded: ticket={ticket_id}, rating={rating}/5")

    # Save the rating as a conversation entry
    db.save_message(phone, "user", f"CSAT rating: {rating}/5", intent="CSAT", lang="en")

    if rating >= 4:
        return "🙏 Thank you for the great rating! We're glad we could help."
    elif rating == 3:
        return "👍 Thanks for your feedback! We'll keep working to improve."
    else:
        return "😔 We're sorry we didn't meet your expectations. Your feedback has been shared with our team."


# ──────────────────────────────────────
# Proactive Message Templates
# ──────────────────────────────────────
def shipping_update_message(order_id: str, status: str, tracking_url: str = "") -> str:
    """Generate a shipping update notification."""
    messages = {
        "shipped": f"📦 Great news! Your order {order_id} has been shipped.\n{f'Track here: {tracking_url}' if tracking_url else ''}",
        "out_for_delivery": f"🚚 Your order {order_id} is out for delivery today! Please keep your phone handy.",
        "delivered": f"✅ Your order {order_id} has been delivered! We hope you love it.\n\nReply '5' if you're happy or '1' if you need help.",
        "delayed": f"⚠️ We're sorry — your order {order_id} is slightly delayed. We're working to get it to you ASAP.",
    }
    return messages.get(status, f"📋 Order {order_id} update: {status}")


def order_confirmation_message(order_id: str, items: list[str], estimated_delivery: str) -> str:
    """Generate an order confirmation notification."""
    items_text = ", ".join(items)
    return (
        f"✅ Order Confirmed!\n\n"
        f"Order ID: {order_id}\n"
        f"Items: {items_text}\n"
        f"Estimated Delivery: {estimated_delivery}\n\n"
        f"You can track your order anytime by sending \"Where is my order?\""
    )


def refund_update_message(order_id: str, status: str, amount: str = "") -> str:
    """Generate a refund status notification."""
    messages = {
        "initiated": f"💸 Refund for order {order_id} has been initiated. {f'Amount: ₹{amount}' if amount else ''}",
        "processing": f"⏳ Your refund for order {order_id} is being processed. It should reflect in 5-7 business days.",
        "completed": f"✅ Your refund for order {order_id} has been credited to your account!{f' Amount: ₹{amount}' if amount else ''}",
    }
    return messages.get(status, f"📋 Refund update for {order_id}: {status}")
