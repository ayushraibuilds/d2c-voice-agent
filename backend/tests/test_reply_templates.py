"""
Unit tests for reply_templates.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from reply_templates import format_reply, get_faq_answer, TEMPLATES


class TestFormatReply:
    def test_basic_english_template(self):
        reply = format_reply("en", "GREETING")
        assert "help" in reply.lower() or "welcome" in reply.lower()

    def test_basic_hindi_template(self):
        reply = format_reply("hi", "GREETING")
        assert reply  # Non-empty
        assert reply != format_reply("en", "GREETING")  # Different from English

    def test_order_status_delivered(self):
        reply = format_reply("en", "ORDER_STATUS_DELIVERED", order_id="ORD-123", delivery_date="March 14")
        assert "ORD-123" in reply
        assert "March 14" in reply

    def test_order_status_pending(self):
        reply = format_reply("en", "ORDER_STATUS_PENDING", order_id="ORD-456", status="Shipped", delivery_date="March 20")
        assert "ORD-456" in reply
        assert "Shipped" in reply
        assert "March 20" in reply

    def test_refund_initiated(self):
        reply = format_reply("en", "REFUND_INITIATED", order_id="ORD-789")
        assert "ORD-789" in reply
        assert "refund" in reply.lower()

    def test_refund_exists(self):
        reply = format_reply("en", "REFUND_EXISTS", status="Processing")
        assert "Processing" in reply

    def test_order_cancelled(self):
        reply = format_reply("en", "ORDER_CANCELLED", order_id="ORD-111")
        assert "ORD-111" in reply

    def test_delivery_complaint_ack(self):
        reply = format_reply("en", "DELIVERY_COMPLAINT_ACK", ticket_id="TKT-ABCD")
        assert "TKT-ABCD" in reply

    def test_human_handoff(self):
        reply = format_reply("en", "HUMAN_HANDOFF")
        assert "human" in reply.lower() or "agent" in reply.lower()

    def test_product_search_results(self):
        products_text = "Product A\n\nProduct B"
        reply = format_reply("en", "PRODUCT_SEARCH_RESULTS", results=products_text)
        assert "Product A" in reply
        assert "Product B" in reply

    def test_product_search_empty(self):
        reply = format_reply("en", "PRODUCT_SEARCH_EMPTY")
        assert reply  # Non-empty response

    def test_fallback_to_english_for_unknown_lang(self):
        reply = format_reply("fr", "GREETING")  # French not supported
        en_reply = format_reply("en", "GREETING")
        assert reply == en_reply

    def test_fallback_for_nonexistent_intent(self):
        reply = format_reply("en", "NONEXISTENT_INTENT")
        assert reply == ""

    def test_hindi_order_status(self):
        reply = format_reply("hi", "ORDER_STATUS_DELIVERED", order_id="ORD-999", delivery_date="15 मार्च")
        assert "ORD-999" in reply

    def test_all_english_intents_exist(self):
        required_intents = [
            "ORDER_STATUS_DELIVERED", "ORDER_STATUS_PENDING", "ORDER_STATUS_NOT_FOUND",
            "REFUND_INITIATED", "REFUND_EXISTS", "REFUND_NOT_POSSIBLE",
            "ORDER_CANCELLED", "ORDER_CANCEL_NOT_POSSIBLE", "EXCHANGE_INITIATED",
            "PAYMENT_ISSUE_ACK", "DELIVERY_COMPLAINT_ACK", "HUMAN_HANDOFF",
            "GREETING", "UNKNOWN", "ERROR", "VOICE_ERROR", "FAQ",
            "PRODUCT_SEARCH_EMPTY", "PRODUCT_SEARCH_RESULTS",
        ]
        for intent in required_intents:
            assert intent in TEMPLATES["en"], f"Missing English template for: {intent}"


class TestGetFaqAnswer:
    def test_return_policy_en(self):
        answer = get_faq_answer("en", "return_policy")
        assert "return" in answer.lower() or "days" in answer.lower()

    def test_shipping_time_en(self):
        answer = get_faq_answer("en", "shipping_time")
        assert "days" in answer.lower() or "shipping" in answer.lower()

    def test_contact_support_en(self):
        answer = get_faq_answer("en", "contact_support")
        assert "1800" in answer or "contact" in answer.lower()

    def test_return_policy_hi(self):
        answer = get_faq_answer("hi", "return_policy")
        assert answer  # Non-empty Hindi answer

    def test_fallback_to_english_for_unknown_lang(self):
        answer_fr = get_faq_answer("fr", "return_policy")
        answer_en = get_faq_answer("en", "return_policy")
        assert answer_fr == answer_en

    def test_unknown_topic_fallback(self):
        answer = get_faq_answer("en", "random_topic")
        assert answer == ""
