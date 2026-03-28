from unittest.mock import patch
from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webhook import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("webhook.verify_twilio_signature", return_value=True)
@patch("webhook.handle_message_task")
def test_whatsapp_webhook_receives_inbound(mock_handle_task, mock_verify):
    response = client.post(
        "/api/v1/whatsapp-webhook",
        headers={"X-Twilio-Signature": "dummy_signature"},
        data={
            "From": "whatsapp:+919876543210",
            "To": "whatsapp:+14155238886",
            "Body": "Where is my order?",
            "NumMedia": "0"
        }
    )
    assert response.status_code == 200
    # Background task should have been added
    content = response.text
    assert "Response" in content  # TwiML xml return check
    mock_handle_task.assert_called_once_with(
        "whatsapp:+919876543210", "whatsapp:+14155238886", "Where is my order?", 0, None, None
    )

@patch("database.get_brand_by_phone")
@patch("webhook.send_whatsapp_message")
def test_e2e_text_message_processing(mock_send, mock_get_brand):
    # Mock the brand lookups
    mock_get_brand.return_value = {
        "whatsapp_number": "+14155238886",
        "name": "Test Brand",
        "custom_prompt": "Test Prompt",
        "api_key": "test_api_key"
    }
    
    # We call the handler directly to test the processing pipeline (LangGraph + NLP)
    from webhook import handle_message_task
    with patch("webhook.process_message", return_value="Your order ORD-123 is on the way.") as mock_process:
        handle_message_task("whatsapp:+919876543210", "whatsapp:+14155238886", "track order ORD-123", 0, None, None)
        
        mock_process.assert_called_once_with("whatsapp:+919876543210", "track order ORD-123", mock_get_brand.return_value, None)
        mock_send.assert_called_once_with("whatsapp:+919876543210", "whatsapp:+14155238886", "Your order ORD-123 is on the way.")

def test_status_callback():
    response = client.post(
        "/api/v1/twilio/status",
        data={
            "MessageSid": "SMxxxx",
            "MessageStatus": "delivered",
            "To": "whatsapp:+919876543210"
        }
    )
    assert response.status_code == 200
    assert response.text == "OK"

@patch("webhook.transcribe_audio_groq", return_value="Where is my order ORD-999?")
@patch("database.get_brand_by_phone")
@patch("webhook.send_whatsapp_message")
def test_e2e_audio_message_processing(mock_send, mock_get_brand, mock_transcribe):
    """Test the full flow from receiving an audio payload to parsing intent and sending response."""
    mock_get_brand.return_value = {
        "whatsapp_number": "+14155238886",
        "name": "Test Brand"
    }
    
    from webhook import handle_message_task
    with patch("webhook.process_message", return_value="ORD-999 is shipped.") as mock_process:
        # Simulate an incoming background task created from a WhatsApp audio file
        handle_message_task(
            "whatsapp:+919876543210", 
            "whatsapp:+14155238886", 
            "", 
            1, 
            "https://api.twilio.com/mock-audio.ogg", 
            "audio/ogg"
        )
        
        mock_transcribe.assert_called_once_with("https://api.twilio.com/mock-audio.ogg")
        mock_process.assert_called_once_with(
            "whatsapp:+919876543210", 
            "Where is my order ORD-999?", 
            mock_get_brand.return_value, 
            None
        )
        mock_send.assert_called_once_with("whatsapp:+919876543210", "whatsapp:+14155238886", "ORD-999 is shipped.")
