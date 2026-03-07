import os
from typing import Dict, TypedDict, Any, Literal
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

import lang_detect
from reply_templates import format_reply, get_faq_answer
import mock_ecommerce

class GraphState(TypedDict):
    sender_phone: str
    message: str
    detected_lang: str
    intent: str
    order_id: str
    reply: str

class IntentClassification(BaseModel):
    intent: str = Field(description="One of: ORDER_STATUS, REFUND_REQUEST, PRODUCT_FAQ, HUMAN_HANDOFF, UNKNOWN")
    order_id: str = Field(description="The order ID if mentioned in the text (e.g. ORD-12345, ORD-11223), else empty string.", default="")

def create_zendesk_ticket_stub(phone: str, message: str, intent: str) -> str:
    """Mock integration: Simulates creating a formal support ticket in Zendesk or Freshdesk."""
    import uuid
    ticket_id = f"ZDK-{str(uuid.uuid4()).split('-')[0].upper()}"
    print(f"\n[ZENDESK API STUB] 🚨 CRITICAL ALERT")
    print(f"[ZENDESK API STUB] New Ticket Created: {ticket_id}")
    print(f"[ZENDESK API STUB] User Phone: {phone}")
    print(f"[ZENDESK API STUB] Intent: {intent}")
    print(f"[ZENDESK API STUB] Final Message: '{message}'")
    print(f"[ZENDESK API STUB] Agent assigned and SLA timer started.\n")
    return ticket_id

def get_llm():
    return ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama3-70b-8192", temperature=0)

def detect_language_node(state: GraphState):
    """Detect the language of the incoming message using hybrid strategy."""
    result = lang_detect.detect(state["message"])
    return {"detected_lang": result.lang_code}

def classify_intent_node(state: GraphState):
    """Use LLM to classify intent into 5 strict paths and extract order_id."""
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(IntentClassification)
        
        prompt = f"""You are an intent classifier for an Indian D2C brand WhatsApp support bot.
Classify the following user message into EXACTLY ONE of the allowed intents.
If an order ID (like ORD-12345 or ORD-67890) is present in the message, extract it into order_id. 
If no order ID is found, leave it as an empty string.

User Message: "{state['message']}"
"""
        result = structured_llm.invoke(prompt)
        intent = result.intent
        if intent not in ["ORDER_STATUS", "REFUND_REQUEST", "PRODUCT_FAQ", "HUMAN_HANDOFF"]:
            intent = "UNKNOWN"
            
        return {"intent": intent, "order_id": result.order_id}
    except Exception as e:
        print(f"Classification error: {e}")
        return {"intent": "UNKNOWN", "order_id": ""}

def route_intent(state: GraphState) -> str:
    """Route to the appropriate action node based on intent."""
    return state["intent"]

def handle_order_status(state: GraphState):
    """Fetch order status from mock_ecommerce database."""
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    order_id = state["order_id"]
    
    # Try fetching by order_id first, then by phone
    order = mock_ecommerce.get_order_by_id(order_id) if order_id else mock_ecommerce.get_order_by_phone(phone)
    
    if not order:
        reply = format_reply(lang, "ORDER_STATUS_NOT_FOUND")
    elif order["status"] == "Delivered":
        reply = format_reply(lang, "ORDER_STATUS_DELIVERED", order_id=order["order_id"], delivery_date=order["estimated_delivery"])
    else:
        reply = format_reply(lang, "ORDER_STATUS_PENDING", order_id=order["order_id"], status=order["status"], delivery_date=order["estimated_delivery"])
        
    return {"reply": reply}

def handle_refund_request(state: GraphState):
    """Process refund using mock_ecommerce database."""
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    order_id = state["order_id"]
    
    order = mock_ecommerce.get_order_by_id(order_id) if order_id else mock_ecommerce.get_order_by_phone(phone)
    
    if not order:
        reply = format_reply(lang, "ORDER_STATUS_NOT_FOUND")
    else:
        result = mock_ecommerce.process_refund(order["order_id"])
        if result["success"]:
            reply = format_reply(lang, "REFUND_INITIATED", order_id=order["order_id"])
        elif "already in status" in result["message"]:
            reply = format_reply(lang, "REFUND_EXISTS", status=order["refund_status"])
        else:
            reply = format_reply(lang, "REFUND_NOT_POSSIBLE", status=order["status"])
            
    return {"reply": reply}

def handle_faq(state: GraphState):
    """Answer product FAQ."""
    lang = state["detected_lang"]
    # For a real implementation, we would use RAG or a vector DB. 
    # Here, we default to the return policy for simplicity.
    answer = get_faq_answer(lang, "return_policy")
    reply = format_reply(lang, "FAQ", answer=answer)
    return {"reply": reply}

def handle_handoff(state: GraphState):
    """Perform human agent handoff and create a support ticket."""
    lang = state["detected_lang"]
    phone = state["sender_phone"]
    message = state["message"]
    
    # Fire the enterprise stub
    ticket_id = create_zendesk_ticket_stub(phone, message, "HUMAN_HANDOFF")
    
    reply = format_reply(lang, "HUMAN_HANDOFF")
    # Append ticket ID to reply
    if lang == "hi":
        reply += f"\n(Ticket ID: {ticket_id})"
    else:
        reply += f"\n(Ticket ID: {ticket_id})"
        
    return {"reply": reply}

def handle_unknown(state: GraphState):
    """Fallback when intent is unknown."""
    lang = state["detected_lang"]
    reply = format_reply(lang, "UNKNOWN")
    return {"reply": reply}

# Build Graph
builder = StateGraph(GraphState)

# Add Nodes
builder.add_node("detect_language", detect_language_node)
builder.add_node("classify", classify_intent_node)
builder.add_node("ORDER_STATUS", handle_order_status)
builder.add_node("REFUND_REQUEST", handle_refund_request)
builder.add_node("PRODUCT_FAQ", handle_faq)
builder.add_node("HUMAN_HANDOFF", handle_handoff)
builder.add_node("UNKNOWN", handle_unknown)

# Edges
builder.set_entry_point("detect_language")
builder.add_edge("detect_language", "classify")

builder.add_conditional_edges("classify", route_intent, {
    "ORDER_STATUS": "ORDER_STATUS",
    "REFUND_REQUEST": "REFUND_REQUEST",
    "PRODUCT_FAQ": "PRODUCT_FAQ",
    "HUMAN_HANDOFF": "HUMAN_HANDOFF",
    "UNKNOWN": "UNKNOWN"
})

builder.add_edge("ORDER_STATUS", END)
builder.add_edge("REFUND_REQUEST", END)
builder.add_edge("PRODUCT_FAQ", END)
builder.add_edge("HUMAN_HANDOFF", END)
builder.add_edge("UNKNOWN", END)

# Compile Graph
graph = builder.compile()

def process_message(sender_phone: str, message: str) -> str:
    """Entry point to process a message through the LangGraph timeline."""
    if not message.strip():
        return format_reply("en", "UNKNOWN")
        
    initial_state = {
        "sender_phone": sender_phone,
        "message": message,
        "detected_lang": "",
        "intent": "",
        "order_id": "",
        "reply": ""
    }
    
    try:
        final_state = graph.invoke(initial_state)
        return final_state["reply"]
    except Exception as e:
        print(f"Graph Execution Error: {e}")
        return format_reply("en", "ERROR")
