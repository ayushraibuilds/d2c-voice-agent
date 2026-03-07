import os
import requests
import tempfile
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from groq import Groq
from support_graph import process_message

app = FastAPI(title="D2C Voice-First Agent Webhook")

def transcribe_audio_groq(media_url: str) -> str:
    """Download audio from Twilio and transcribe using Groq's whisper-large-v3."""
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
    
    if not twilio_sid or not twilio_auth:
        print("Missing Twilio credentials for downloading media.")
        return ""
        
    response = requests.get(media_url, auth=(twilio_sid, twilio_auth))
    if response.status_code != 200:
        print(f"Failed to download media from Twilio. Status: {response.status_code}")
        return ""
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_audio:
        tmp_audio.write(response.content)
        tmp_audio_path = tmp_audio.name
        
    try:
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        with open(tmp_audio_path, "rb") as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=("audio.ogg", audio_file.read()),
                model="whisper-large-v3",
                response_format="text"
            )
        return transcription
    except Exception as e:
        print(f"Transcription Error: {e}")
        return ""
    finally:
        if os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)

def send_whatsapp_message(to_number: str, from_number: str, body: str):
    """Send a reply via Twilio WhatsApp API."""
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
    if not twilio_sid or not twilio_auth:
        print("Missing Twilio credentials for sending.")
        return
        
    client = Client(twilio_sid, twilio_auth)
    try:
        client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
    except Exception as e:
        print(f"Twilio Error: {e}")

def handle_message_task(sender_phone: str, twilio_phone: str, text: str, num_media: int, media_url: str, media_type: str):
    """Background task to process the message and send a reply."""
    message_text = text.strip() if text else ""
    
    # Handle Voice Notes (audio)
    if num_media > 0 and media_type and "audio" in media_type:
        print(f"Received audio message. Transcribing...")
        message_text = transcribe_audio_groq(media_url)
        print(f"Transcription result: {message_text}")
        if not message_text:
            from reply_templates import format_reply
            error_response = format_reply("en", "VOICE_ERROR")
            send_whatsapp_message(sender_phone, twilio_phone, error_response)
            return
            
    # Process text through the main support LangGraph
    reply_text = process_message(sender_phone, message_text)
    
    # Send the reply back to the user
    send_whatsapp_message(sender_phone, twilio_phone, reply_text)

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    Body: str = Form(""),
    From: str = Form(""),
    To: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None)
):
    """Endpoint for Twilio WhatsApp Webhook."""
    # Acknowledge receipt to Twilio immediately to avoid timeouts (15s limit)
    twiml_response = MessagingResponse()
    
    # Process asynchronously
    background_tasks.add_task(handle_message_task, From, To, Body, NumMedia, MediaUrl0, MediaContentType0)
    
    return PlainTextResponse(str(twiml_response), media_type="text/xml")
