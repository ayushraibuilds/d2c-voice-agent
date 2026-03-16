"""
LangGraph State Machine for D2C WhatsApp Support.

Nodes:
  1. detect_language — hybrid heuristic + langdetect
  2. classify — LLM-based intent classification with sanitized input
  3. sentiment — analyze sentiment, auto-escalate if critical
  4. Action nodes — one per intent, using e-commerce adapter + database

Intents: ORDER_STATUS, REFUND_REQUEST, ORDER_CANCEL, EXCHANGE_REQUEST,
         PAYMENT_ISSUE, DELIVERY_COMPLAINT, PRODUCT_FAQ, HUMAN_HANDOFF,
         GREETING, UNKNOWN
"""

import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from config import get_settings
from logger import get_logger, set_request_id
from ecommerce_adapter import get_adapter
from sentiment import analyze_sentiment, should_auto_escalate
from notifications import is_csat_response, process_csat_response
import database as db
import lang_detect
import webhook_dispatcher
from reply_templates import format_reply, get_faq_answer

settings = get_settings()
log = get_logger()

# ──────────────────────────────────────────────
# Singleton LLM client (created once, reused)
# ──────────────────────────────────────────────
_llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
)


def get_llm() -> ChatGroq:
    """Return the singleton LLM instance."""
    return _llm


# ──────────────────────────────────────────────
# Input Sanitization
# ──────────────────────────────────────────────
_DANGEROUS_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)",
    r"you\s+are\s+now\s+(?:a\s+)?(?:DAN|jailbreak|unrestricted)",
    r"system\s*:\s*",
    r"<\|(?:im_start|im_end|system|user|assistant)\|>",
    r"\[INST\]",
    r"```\s*system",
]
_INJECTION_RE = re.compile("|".join(_DANGEROUS_PATTERNS), re.IGNORECASE)

MAX_MESSAGE_LENGTH = 2000


def sanitize_input(text: str) -> str:
    """Sanitize user input before passing to LLM."""
    if not text:
        return ""
    text = text[:MAX_MESSAGE_LENGTH]
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    text = _INJECTION_RE.sub("[filtered]", text)
    return text.strip()


# ──────────────────────────────────────────────
# Graph State
# ──────────────────────────────────────────────
class GraphState(TypedDict):
    sender_phone: str
    message: str
    detected_lang: str
    intent: str
    order_id: str
    conversation_context: str
    sentiment: str
    brand_name: str
    brand_custom_prompt: str
    brand_webhook_url: str
    reply: str


VALID_INTENTS = [
    "ORDER_STATUS",
    "REFUND_REQUEST",
    "ORDER_CANCEL",
    "EXCHANGE_REQUEST",
    "PAYMENT_ISSUE",
    "DELIVERY_COMPLAINT",
    "PRODUCT_FAQ",
    "HUMAN_HANDOFF",
    "GREETING",
]


# ──────────────────────────────────────────────
# Structured Output Schema
# ──────────────────────────────────────────────
class IntentClassification(BaseModel):
    intent: str = Field(
        description="One of: ORDER_STATUS, REFUND_REQUEST, ORDER_CANCEL, EXCHANGE_REQUEST, PAYMENT_ISSUE, DELIVERY_COMPLAINT, PRODUCT_FAQ, HUMAN_HANDOFF, GREETING, UNKNOWN"
    )
    order_id: str = Field(
        description="The order ID if mentioned (e.g. ORD-12345), else empty string.",
        default="",
    )
    faq_topic: str = Field(
        description="If PRODUCT_FAQ: one of return_policy, shipping_time, contact_support, general. Else empty.",
        default="",
    )


# ──────────────────────────────────────────────
# Graph Nodes
# ──────────────────────────────────────────────
def detect_language_node(state: GraphState):
    """Detect the language of the incoming message."""
    result = lang_detect.detect(state["message"])
    log.info(f"Language detected: {result.lang_code} (method={result.method}, conf={result.confidence})")
    return {"detected_lang": result.lang_code}


def load_context_node(state: GraphState):
    """Load conversation history for multi-turn context."""
    context = db.get_conversation_summary(state["sender_phone"], limit=5)
    if context:
        log.info(f"Loaded {len(context.splitlines())} previous messages for context")
    return {"conversation_context": context}


def classify_intent_node(state: GraphState):
    """Use LLM to classify intent with conversation context."""
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(IntentClassification)

        sanitized_message = sanitize_input(state["message"])
        context = state.get("conversation_context", "")

        context_block = ""
        if context:
            context_block = f"""
Recent conversation history (for context):
{context}

"""

        brand_context = ""
        if state.get("brand_name"):
            brand_context = f"You are assisting customers of: {state['brand_name']}.\n"
        if state.get("brand_custom_prompt"):
            brand_context += f"Brand Instructions: {state['brand_custom_prompt']}\n"

        prompt = f"""You are an intent classifier for an Indian D2C brand WhatsApp support bot.
{brand_context}
Classify the following user message into EXACTLY ONE of the allowed intents.

Rules:
- Greeting (hi/hello/namaste) → GREETING
- Order status, tracking, delivery → ORDER_STATUS
- Refund, money back → REFUND_REQUEST
- Cancel order → ORDER_CANCEL
- Exchange, swap, replace product → EXCHANGE_REQUEST
- Payment failed, double charge, payment issue → PAYMENT_ISSUE
- Delivery complaint, damaged product, late delivery → DELIVERY_COMPLAINT
- Return policy, shipping time, contact info, product questions → PRODUCT_FAQ
  - Also set faq_topic: return_policy, shipping_time, contact_support, or general
- Speak to human/agent/manager → HUMAN_HANDOFF
- Otherwise → UNKNOWN

Extract order_id if present (e.g. ORD-12345). If none found, leave empty.
{context_block}
Current user message: "{sanitized_message}"
"""
        result = structured_llm.invoke(prompt)
        intent = result.intent if result.intent in VALID_INTENTS else "UNKNOWN"

        log.info(f"Intent classified: {intent} (order_id={result.order_id})")

        # Save user message to conversation history
        db.save_message(
            state["sender_phone"], "user", state["message"],
            intent=intent, lang=state["detected_lang"]
        )

        return {"intent": intent, "order_id": result.order_id}
    except Exception as e:
        log.error(f"Classification error: {e}")
        return {"intent": "UNKNOWN", "order_id": ""}


def sentiment_node(state: GraphState):
    """Analyze sentiment and auto-escalate if needed."""
    message = state["message"]
    phone = state["sender_phone"]
    current_sentiment = analyze_sentiment(message)

    # Check conversation history for repeated negative sentiment
    history = db.get_conversation_history(phone, limit=10)
    past_sentiments = [
        analyze_sentiment(m["message"])
        for m in history if m["role"] == "user"
    ]

    if should_auto_escalate(current_sentiment, past_sentiments):
        log.warning(f"Auto-escalating {phone} due to {current_sentiment.value} sentiment")
        return {"sentiment": current_sentiment.value, "intent": "HUMAN_HANDOFF"}

    return {"sentiment": current_sentiment.value}


def route_intent(state: GraphState) -> str:
    """Route to the appropriate action node based on intent."""
    return state["intent"]


# ─── Action Nodes ───

def handle_order_status(state: GraphState):
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    order_id = state["order_id"]
    adapter = get_adapter()

    order = adapter.get_order_by_id(order_id) if order_id else adapter.get_order_by_phone(phone)

    if not order:
        reply = format_reply(lang, "ORDER_STATUS_NOT_FOUND")
    elif order["status"] == "Delivered":
        reply = format_reply(lang, "ORDER_STATUS_DELIVERED", order_id=order["order_id"], delivery_date=order["estimated_delivery"])
    else:
        reply = format_reply(lang, "ORDER_STATUS_PENDING", order_id=order["order_id"], status=order["status"], delivery_date=order["estimated_delivery"])

    return {"reply": reply}


def handle_refund_request(state: GraphState):
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    order_id = state["order_id"]
    adapter = get_adapter()

    order = adapter.get_order_by_id(order_id) if order_id else adapter.get_order_by_phone(phone)

    if not order:
        reply = format_reply(lang, "ORDER_STATUS_NOT_FOUND")
    else:
        result = adapter.process_refund(order["order_id"])
        if result["success"]:
            reply = format_reply(lang, "REFUND_INITIATED", order_id=order["order_id"])
        elif "already in status" in result["message"]:
            reply = format_reply(lang, "REFUND_EXISTS", status=order["refund_status"])
        else:
            reply = format_reply(lang, "REFUND_NOT_POSSIBLE", status=order["status"])

    return {"reply": reply}


def handle_order_cancel(state: GraphState):
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    order_id = state["order_id"]
    adapter = get_adapter()

    order = adapter.get_order_by_id(order_id) if order_id else adapter.get_order_by_phone(phone)

    if not order:
        reply = format_reply(lang, "ORDER_STATUS_NOT_FOUND")
    else:
        result = adapter.cancel_order(order["order_id"])
        if result["success"]:
            reply = format_reply(lang, "ORDER_CANCELLED", order_id=order["order_id"])
        else:
            reply = format_reply(lang, "ORDER_CANCEL_NOT_POSSIBLE", status=order["status"])

    return {"reply": reply}


def handle_exchange_request(state: GraphState):
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    order_id = state["order_id"]
    adapter = get_adapter()

    order = adapter.get_order_by_id(order_id) if order_id else adapter.get_order_by_phone(phone)

    if not order:
        reply = format_reply(lang, "ORDER_STATUS_NOT_FOUND")
    else:
        # Create a ticket for the exchange
        db.create_ticket(phone, state["message"], "EXCHANGE_REQUEST")
        reply = format_reply(lang, "EXCHANGE_INITIATED", order_id=order["order_id"])

    return {"reply": reply}


def handle_payment_issue(state: GraphState):
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    order_id = state["order_id"]
    adapter = get_adapter()

    order = adapter.get_order_by_id(order_id) if order_id else adapter.get_order_by_phone(phone)

    if not order:
        reply = format_reply(lang, "ORDER_STATUS_NOT_FOUND")
    else:
        ticket_id = db.create_ticket(phone, state["message"], "PAYMENT_ISSUE")
        reply = format_reply(lang, "PAYMENT_ISSUE_ACK", order_id=order["order_id"])

    return {"reply": reply}


def handle_delivery_complaint(state: GraphState):
    lang = state["detected_lang"]
    phone = state["sender_phone"]

    ticket_id = db.create_ticket(phone, state["message"], "DELIVERY_COMPLAINT")
    reply = format_reply(lang, "DELIVERY_COMPLAINT_ACK", ticket_id=ticket_id)

    return {"reply": reply}


def handle_faq(state: GraphState):
    """Answer product FAQ — routes to the correct topic."""
    lang = state["detected_lang"]
    message_lower = state["message"].lower()

    if any(kw in message_lower for kw in ["return", "wapas", "exchange", "replace"]):
        topic = "return_policy"
    elif any(kw in message_lower for kw in ["shipping", "delivery time", "kitne din", "kab aayega", "ship"]):
        topic = "shipping_time"
    elif any(kw in message_lower for kw in ["contact", "call", "phone", "number", "email", "support"]):
        topic = "contact_support"
    else:
        topic = "return_policy"

    answer = get_faq_answer(lang, topic)
    reply = format_reply(lang, "FAQ", answer=answer)
    return {"reply": reply}


def handle_greeting(state: GraphState):
    lang = state["detected_lang"]
    reply = format_reply(lang, "GREETING")
    return {"reply": reply}


def handle_handoff(state: GraphState):
    lang = state["detected_lang"]
    phone = state["sender_phone"]

    ticket_id = db.create_ticket(phone, state["message"], "HUMAN_HANDOFF")
    reply = format_reply(lang, "HUMAN_HANDOFF")
    reply += f"\n(Ticket ID: {ticket_id})"
    
    # ── Fire Webhook Event ──
    webhook_url = state.get("brand_webhook_url")
    if webhook_url:
        webhook_dispatcher.dispatch_event(webhook_url, "ticket.created", {
            "ticket_id": ticket_id,
            "phone": phone,
            "intent": "HUMAN_HANDOFF",
            "message": state["message"]
        })

    return {"reply": reply}


def handle_unknown(state: GraphState):
    lang = state["detected_lang"]
    reply = format_reply(lang, "UNKNOWN")
    return {"reply": reply}


# ──────────────────────────────────────────────
# Build Graph
# ──────────────────────────────────────────────
builder = StateGraph(GraphState)

# Nodes
builder.add_node("detect_language", detect_language_node)
builder.add_node("load_context", load_context_node)
builder.add_node("classify", classify_intent_node)
builder.add_node("sentiment", sentiment_node)
builder.add_node("ORDER_STATUS", handle_order_status)
builder.add_node("REFUND_REQUEST", handle_refund_request)
builder.add_node("ORDER_CANCEL", handle_order_cancel)
builder.add_node("EXCHANGE_REQUEST", handle_exchange_request)
builder.add_node("PAYMENT_ISSUE", handle_payment_issue)
builder.add_node("DELIVERY_COMPLAINT", handle_delivery_complaint)
builder.add_node("PRODUCT_FAQ", handle_faq)
builder.add_node("HUMAN_HANDOFF", handle_handoff)
builder.add_node("GREETING", handle_greeting)
builder.add_node("UNKNOWN", handle_unknown)

# Edges: detect_lang → load_context → classify → sentiment → route
builder.set_entry_point("detect_language")
builder.add_edge("detect_language", "load_context")
builder.add_edge("load_context", "classify")
builder.add_edge("classify", "sentiment")

builder.add_conditional_edges(
    "sentiment",
    route_intent,
    {
        "ORDER_STATUS": "ORDER_STATUS",
        "REFUND_REQUEST": "REFUND_REQUEST",
        "ORDER_CANCEL": "ORDER_CANCEL",
        "EXCHANGE_REQUEST": "EXCHANGE_REQUEST",
        "PAYMENT_ISSUE": "PAYMENT_ISSUE",
        "DELIVERY_COMPLAINT": "DELIVERY_COMPLAINT",
        "PRODUCT_FAQ": "PRODUCT_FAQ",
        "HUMAN_HANDOFF": "HUMAN_HANDOFF",
        "GREETING": "GREETING",
        "UNKNOWN": "UNKNOWN",
    },
)

for intent in [
    "ORDER_STATUS", "REFUND_REQUEST", "ORDER_CANCEL", "EXCHANGE_REQUEST",
    "PAYMENT_ISSUE", "DELIVERY_COMPLAINT", "PRODUCT_FAQ", "HUMAN_HANDOFF",
    "GREETING", "UNKNOWN",
]:
    builder.add_edge(intent, END)

# Compile
graph = builder.compile()


def process_message(sender_phone: str, message: str, brand_config: dict | None = None) -> str:
    """Entry point to process a message through the LangGraph pipeline."""
    request_id = set_request_id()
    log.info(f"Processing message from {sender_phone} (request_id={request_id})")

    if not message.strip():
        return format_reply("en", "UNKNOWN")

    # ── CSAT interception: if user is responding to a rating request ──
    if is_csat_response(sender_phone, message):
        return process_csat_response(sender_phone, message)

    brand_config = brand_config or {}

    initial_state: GraphState = {
        "sender_phone": sender_phone,
        "message": message,
        "detected_lang": "",
        "intent": "",
        "order_id": "",
        "conversation_context": "",
        "sentiment": "",
        "brand_name": brand_config.get("name", "D2C Brand"),
        "brand_custom_prompt": brand_config.get("custom_prompt", ""),
        "brand_webhook_url": brand_config.get("webhook_url", ""),
        "reply": "",
    }

    try:
        final_state = graph.invoke(initial_state)
        reply = final_state["reply"]

        # Save assistant reply to conversation history
        db.save_message(
            sender_phone, "assistant", reply,
            intent=final_state.get("intent", ""),
            lang=final_state.get("detected_lang", "en"),
        )

        log.info(
            f"Reply sent: intent={final_state['intent']}, "
            f"lang={final_state['detected_lang']}, "
            f"sentiment={final_state.get('sentiment', 'n/a')}"
        )
        return reply
    except Exception as e:
        log.error(f"Graph execution error: {e}")
        return format_reply("en", "ERROR")
