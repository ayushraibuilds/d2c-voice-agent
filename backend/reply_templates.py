"""
Multilingual reply templates for D2C WhatsApp Support.

Currently ships with Hindi (hi) and English (en).
Other languages (ta, te, kn, bn) have stub templates that fall back to English.
"""

TEMPLATES = {
    "en": {
        "ORDER_STATUS_DELIVERED": "📦 Your order {order_id} was delivered on {delivery_date}.",
        "ORDER_STATUS_PENDING": "🚚 Your order {order_id} is currently '{status}'. It is expected to arrive by {delivery_date}.",
        "ORDER_STATUS_NOT_FOUND": "🔍 We couldn't find an active order. Please provide your Order ID (e.g., ORD-12345).",
        "REFUND_INITIATED": "💸 Refund for order {order_id} has been initiated successfully.",
        "REFUND_EXISTS": "ℹ️ Your refund is already in status: {status}.",
        "REFUND_NOT_POSSIBLE": "⚠️ Refunds are not applicable because your order status is '{status}'.",
        "ORDER_CANCELLED": "✅ Your order {order_id} has been cancelled and a refund has been initiated.",
        "ORDER_CANCEL_NOT_POSSIBLE": "⚠️ We cannot cancel this order because it is currently '{status}'.",
        "EXCHANGE_INITIATED": "🔄 Exchange request for order {order_id} has been noted. Our team will reach out shortly.",
        "PAYMENT_ISSUE_ACK": "💳 We've logged your payment issue for order {order_id}. Our finance team will investigate — you'll receive an update within 24 hours.",
        "DELIVERY_COMPLAINT_ACK": "📋 We're sorry to hear about the issue with your delivery. Ticket {ticket_id} has been created and our team will resolve this ASAP.",
        "HUMAN_HANDOFF": "👨‍💻 I am transferring you to a human agent. They will assist you shortly.",
        "GREETING": (
            "👋 Hey there! Welcome to our support. I can help you with:\n"
            "• Order tracking\n"
            "• Refunds & returns\n"
            "• Product info\n"
            "How can I help you today?"
        ),
        "UNKNOWN": (
            "🤔 I didn't quite catch that. You can ask me things like:\n"
            "• \"Where is my order?\"\n"
            "• \"I want to cancel my order and get a refund\"\n"
            "• \"Can I talk to a human?\"\n"
            "• \"Show me your smartwatches\""
        ),
        "PRODUCT_SEARCH_EMPTY": "🔍 I couldn't find any products matching your search. Try adjusting your query!",
        "PRODUCT_SEARCH_RESULTS": "🛒 Here's what I found for you:\n\n{results}\n\nReply to me with what you'd like to order!",
        "ERROR": "⚠️ Our support system is currently experiencing issues. Please try again later.",
        "VOICE_ERROR": "⚠️ We couldn't transcribe your voice note clearly. Please type your message or try again.",
        "FAQ": "ℹ️ {answer}",
    },
    "hi": {
        "ORDER_STATUS_DELIVERED": "📦 आपका ऑडर {order_id} {delivery_date} को डिलीवर हो गया था।",
        "ORDER_STATUS_PENDING": "🚚 आपका ऑडर {order_id} अभी '{status}' है। इसके {delivery_date} तक पहुंचने की उम्मीद है।",
        "ORDER_STATUS_NOT_FOUND": "🔍 हमें कोई एक्टिव ऑडर नहीं मिला। कृपया अपना ऑडर ID (जैसे ORD-12345) बताएं।",
        "REFUND_INITIATED": "💸 ऑडर {order_id} के लिए रिफंड सफलतापूर्वक शुरू कर दिया गया है।",
        "REFUND_EXISTS": "ℹ️ आपके रिफंड का स्टेटस अभी यह है: {status}।",
        "REFUND_NOT_POSSIBLE": "⚠️ रिफंड संभव नहीं है क्योंकि आपका ऑडर स्टेटस '{status}' है।",
        "ORDER_CANCELLED": "✅ आपका ऑडर {order_id} कैंसल कर दिया गया है और रिफंड शुरू कर दिया गया है।",
        "ORDER_CANCEL_NOT_POSSIBLE": "⚠️ हम इस ऑडर को कैंसल नहीं कर सकते क्योंकि इसका स्टेटस '{status}' है।",
        "EXCHANGE_INITIATED": "🔄 ऑडर {order_id} के लिए एक्सचेंज रिक्वेस्ट नोट कर ली गई है। हमारी टीम जल्द ही संपर्क करेगी।",
        "PAYMENT_ISSUE_ACK": "💳 आपकी पेमेंट समस्या ऑडर {order_id} के लिए दर्ज कर ली गई है। हमारी फाइनेंस टीम 24 घंटे में अपडेट देगी।",
        "DELIVERY_COMPLAINT_ACK": "📋 आपकी डिलीवरी में हुई दिक्कत के लिए माफी। टिकट {ticket_id} बनाया गया है, हमारी टीम जल्द से जल्द इसे सुलझाएगी।",
        "HUMAN_HANDOFF": "👨‍💻 मैं आपको एक ह्यूमन एजेंट से कनेक्ट कर रहा हूं। वे जल्द ही आपकी मदद करेंगे।",
        "GREETING": (
            "👋 नमस्ते! हमारे सपोर्ट में आपका स्वागत है। मैं इनमें मदद कर सकता हूं:\n"
            "• ऑर्डर ट्रैकिंग\n"
            "• रिफंड और रिटर्न\n"
            "• प्रोडक्ट जानकारी\n"
            "मैं आपकी कैसे मदद कर सकता हूं?"
        ),
        "UNKNOWN": (
            "🤔 माफ करें, मैं समझ नहीं पाया। आप मुझसे ऐसे सवाल पूछ सकते हैं:\n"
            "• \"Mera order kahan hai?\"\n"
            "• \"Mujhe refund chahiye\"\n"
            "• \"Customer care se baat karni hai\"\n"
            "• \"Koyi naye products dikhao\""
        ),
        "PRODUCT_SEARCH_EMPTY": "🔍 मुझे आपकी खोज से मेल खाता कोई उत्पाद नहीं मिला। कृपया कुछ और खोजें।",
        "PRODUCT_SEARCH_RESULTS": "🛒 यहाँ आपके लिए कुछ उत्पाद हैं:\n\n{results}\n\nआप जो ऑर्डर करना चाहते हैं, मुझे बताएं!",
        "ERROR": "⚠️ हमारे सपोर्ट सिस्टम में अभी कुछ दिक्कत है। कृपया थोड़ी देर बाद कोशिश करें।",
        "VOICE_ERROR": "⚠️ हम आपका वॉइस नोट साफ नहीं सुन पाए। कृपया अपना मैसेज टाइप करें।",
        "FAQ": "ℹ️ {answer}",
    },
    # --- Stub templates for future languages (fall back to English) ---
    "ta": {},
    "te": {},
    "kn": {},
    "bn": {},
}

# Pre-built FAQ answers (English + Hindi)
FAQ_ANSWERS = {
    "en": {
        "return_policy": "📦 You can return items within 7 days of delivery. Keep original tags and packaging intact.",
        "shipping_time": "🚚 Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days.",
        "contact_support": "📞 You can reach our toll-free support at 1800-123-4567 from 9 AM to 6 PM.",
    },
    "hi": {
        "return_policy": "📦 आप डिलीवरी के 7 दिनों के भीतर आइटम वापस (return) कर सकते हैं। प्रोडक्ट के टैग और पैकेजिंग सुरक्षित रखें।",
        "shipping_time": "🚚 नॉर्मल शिपिंग (Standard shipping) में 3-5 दिन लगते हैं। एक्सप्रेस शिपिंग में 1-2 दिन लगते हैं।",
        "contact_support": "📞 आप सुबह 9 बजे से शाम 6 बजे तक हमारे टोल-फ्री सपोर्ट 1800-123-4567 पर कॉल कर सकते हैं।",
    },
}


def format_reply(lang_code: str, intent: str, **kwargs) -> str:
    """
    Format a reply using the appropriate language template.
    Falls back to English if the language or intent isn't available.
    """
    lang_templates = TEMPLATES.get(lang_code, {})
    # Fall back to English if template not found for this language
    template = lang_templates.get(intent) or TEMPLATES["en"].get(intent, "")
    if not template:
        return ""
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        # If format args are missing, return template as-is
        return template


def get_faq_answer(lang_code: str, topic: str) -> str:
    """Get a localized FAQ answer for the given topic."""
    lang_faqs = FAQ_ANSWERS.get(lang_code, FAQ_ANSWERS["en"])
    return lang_faqs.get(topic, FAQ_ANSWERS["en"].get(topic, ""))
