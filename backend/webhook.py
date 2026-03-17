import os
import time
import tempfile
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilio.request_validator import RequestValidator
from groq import Groq
from config import get_settings
from logger import get_logger, set_request_id
from support_graph import process_message
import database as db
import webhook_dispatcher
import sentry_sdk

settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

log = get_logger()

# ──────────────────────────────────────
# Rate Limiter
# ──────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


# ──────────────────────────────────────
# App Lifecycle
# ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and dispatchers on startup."""
    log.info("Starting D2C Voice-First Agent...")
    db.init_db()
    webhook_dispatcher.start_webhook_worker()
    log.info("Server ready. Webhook dispatcher running.")
    yield
    log.info("Shutting down.")


app = FastAPI(
    title="D2C Voice-First Agent",
    description="Voice-first WhatsApp AI Support Agent for Indian D2C brands",
    version=settings.app_version,
    lifespan=lifespan,
)

# --- Middleware ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Singletons ---
_twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
_twilio_validator = RequestValidator(settings.twilio_auth_token)
_groq_client = Groq(api_key=settings.groq_api_key)


# ──────────────────────────────────────
# Retry Helpers
# ──────────────────────────────────────
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 0.5  # seconds


def _retry(fn, *args, retries=MAX_RETRIES, label="operation", **kwargs):
    """Execute fn with exponential backoff retries."""
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt < retries:
                wait = RETRY_BACKOFF_BASE * (2 ** (attempt - 1))
                log.warning(f"{label} failed (attempt {attempt}/{retries}), retrying in {wait}s: {e}")
                time.sleep(wait)
            else:
                log.error(f"{label} failed after {retries} attempts: {e}")
    raise last_error


# ──────────────────────────────────────
# Core Functions
# ──────────────────────────────────────
def verify_twilio_signature(url: str, params: dict, signature: str) -> bool:
    return _twilio_validator.validate(url, params, signature)


def transcribe_audio_groq(media_url: str) -> str:
    """Download audio from Twilio and transcribe with retries."""
    try:
        response = _retry(
            httpx.get, media_url,
            auth=(settings.twilio_account_sid, settings.twilio_auth_token),
            timeout=30.0,
            label="Twilio media download",
        )
        response.raise_for_status()
    except Exception as e:
        log.error(f"Failed to download media: {e}")
        return ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_audio:
        tmp_audio.write(response.content)
        tmp_audio_path = tmp_audio.name

    try:
        with open(tmp_audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        def _transcribe():
            return _groq_client.audio.transcriptions.create(
                file=("audio.ogg", audio_bytes),
                model=settings.whisper_model,
                response_format="text",
            )

        transcription = _retry(_transcribe, label="Groq transcription")
        return transcription
    except Exception as e:
        log.error(f"Transcription failed: {e}")
        return ""
    finally:
        if os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)


def send_whatsapp_message(to_number: str, from_number: str, body: str):
    """Send a reply via Twilio with retries."""
    def _send():
        _twilio_client.messages.create(body=body, from_=from_number, to=to_number)

    try:
        _retry(_send, label="Twilio send")
        log.info(f"Reply sent to {to_number} ({len(body)} chars)")
    except Exception as e:
        log.error(f"Twilio send failed after retries: {e}")


def handle_message_task(
    sender_phone: str, twilio_phone: str, text: str,
    num_media: int, media_url: str, media_type: str,
):
    """Background task to process the message and send a reply."""
    request_id = set_request_id()
    log.info(f"Handling message from {sender_phone} (rid={request_id})")

    message_text = text.strip() if text else ""
    image_url = None

    if num_media > 0 and media_type:
        if "audio" in media_type:
            log.info("Audio message received. Transcribing...")
            message_text = transcribe_audio_groq(media_url)
            if message_text:
                log.info(f"Transcription: {message_text[:80]}...")
            if not message_text:
                from reply_templates import format_reply
                send_whatsapp_message(sender_phone, twilio_phone, format_reply("en", "VOICE_ERROR"))
                return
        elif media_type.startswith("image/"):
            log.info(f"Image message received: {media_url}")
            image_url = media_url

    # Look up brand configuration mapping
    brand_config = db.get_brand_by_phone(twilio_phone)
    if not brand_config:
        log.warning(f"No brand configured for number {twilio_phone}. Using defaults.")

    reply_text = process_message(sender_phone, message_text, brand_config, image_url)
    send_whatsapp_message(sender_phone, twilio_phone, reply_text)


# ──────────────────────────────────────
# API v1 Endpoints
# ──────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.app_version}


@app.get("/api/v1/conversations/{phone}")
@limiter.limit("30/minute")
async def get_conversations(request: Request, phone: str, limit: int = 20):
    """Retrieve conversation history for a phone number."""
    history = db.get_conversation_history(phone, limit)
    return {"phone": phone, "messages": history}


@app.get("/api/v1/tickets")
@limiter.limit("30/minute")
async def get_tickets(request: Request, phone: str | None = None):
    """List open support tickets."""
    tickets = db.get_open_tickets(phone)
    return {"tickets": tickets, "count": len(tickets)}


@app.get("/api/v1/stats")
@limiter.limit("10/minute")
async def get_stats(request: Request):
    """Detailed agent stats for admin dashboard."""
    with db.get_db() as conn:
        total_messages = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        total_tickets = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        open_tickets = conn.execute("SELECT COUNT(*) FROM tickets WHERE status = 'open'").fetchone()[0]
        total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        unique_customers = conn.execute("SELECT COUNT(DISTINCT phone) FROM conversations").fetchone()[0]

        # Intent breakdown
        intent_rows = conn.execute(
            "SELECT intent, COUNT(*) as count FROM conversations WHERE role = 'user' AND intent != '' GROUP BY intent ORDER BY count DESC"
        ).fetchall()
        intent_breakdown = {r["intent"]: r["count"] for r in intent_rows}

        # Language breakdown
        lang_rows = conn.execute(
            "SELECT detected_lang, COUNT(*) as count FROM conversations WHERE role = 'user' AND detected_lang != '' GROUP BY detected_lang ORDER BY count DESC"
        ).fetchall()
        lang_breakdown = {r["detected_lang"]: r["count"] for r in lang_rows}

        # Recent 24h message count
        recent_messages = conn.execute(
            "SELECT COUNT(*) FROM conversations WHERE created_at >= datetime('now', '-1 day')"
        ).fetchone()[0]

    return {
        "total_messages": total_messages,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "total_orders": total_orders,
        "unique_customers": unique_customers,
        "messages_last_24h": recent_messages,
        "intent_breakdown": intent_breakdown,
        "lang_breakdown": lang_breakdown,
    }


@app.get("/api/v1/customers")
@limiter.limit("30/minute")
async def get_customers(request: Request):
    """List all customers with their last message."""
    with db.get_db() as conn:
        rows = conn.execute("""
            SELECT c.phone, c.role, c.message, c.intent, c.created_at,
                   (SELECT COUNT(*) FROM conversations WHERE phone = c.phone) as msg_count
            FROM conversations c
            WHERE c.id IN (
                SELECT MAX(id) FROM conversations GROUP BY phone
            )
            ORDER BY c.created_at DESC
            LIMIT 100
        """).fetchall()
    return {"customers": [dict(r) for r in rows]}


@app.post("/api/v1/tickets/{ticket_id}/close")
@limiter.limit("30/minute")
async def close_ticket_endpoint(request: Request, ticket_id: str):
    """Close a support ticket."""
    success = db.close_ticket(ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    # Fire Webhook Event for ticket closure
    with db.get_db() as conn:
        brand = conn.execute("SELECT webhook_url FROM brands LIMIT 1").fetchone()
        if brand and brand["webhook_url"]:
            webhook_dispatcher.dispatch_event(
                brand["webhook_url"], 
                "ticket.closed", 
                {"ticket_id": ticket_id, "status": "closed"}
            )
            
    return {"status": "closed", "ticket_id": ticket_id}


@app.get("/api/v1/products")
@limiter.limit("30/minute")
async def get_products(request: Request, q: str = "", limit: int = 20):
    """List (or search) the product catalog."""
    products = db.search_products(q, limit=limit)
    return {"products": products, "count": len(products)}


class NotificationRequest(BaseModel):
    """Payload for triggering an outbound WhatsApp notification."""
    phone: str
    type: str  # shipped | out_for_delivery | delivered | delayed | order_confirmation | refund_update
    from_number: str | None = None  # Defaults to first brand number
    data: dict = {}


@app.post("/api/v1/notifications/send")
@limiter.limit("10/minute")
async def send_notification(request: Request, payload: NotificationRequest):
    """Trigger a proactive WhatsApp notification to a customer."""
    import notifications as notif

    notif_type = payload.type
    data = payload.data

    # Format the message based on type
    if notif_type == "shipped":
        message = notif.shipping_update_message(
            data.get("order_id", ""), "shipped", data.get("tracking_url", "")
        )
    elif notif_type == "out_for_delivery":
        message = notif.shipping_update_message(data.get("order_id", ""), "out_for_delivery")
    elif notif_type == "delivered":
        message = notif.shipping_update_message(data.get("order_id", ""), "delivered")
    elif notif_type == "delayed":
        message = notif.shipping_update_message(data.get("order_id", ""), "delayed")
    elif notif_type == "order_confirmation":
        message = notif.order_confirmation_message(
            data.get("order_id", ""),
            data.get("items", []),
            data.get("estimated_delivery", "")
        )
    elif notif_type == "refund_update":
        message = notif.refund_update_message(
            data.get("order_id", ""),
            data.get("status", ""),
            data.get("amount", "")
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unknown notification type: {notif_type}")

    # Resolve sender number (use payload.from_number or first registered brand)
    from_number = payload.from_number
    if not from_number:
        with db.get_db() as conn:
            brand = conn.execute("SELECT whatsapp_number FROM brands LIMIT 1").fetchone()
            from_number = brand["whatsapp_number"] if brand else None

    if not from_number:
        raise HTTPException(status_code=422, detail="No sender phone number configured")

    send_whatsapp_message(payload.phone, from_number, message)
    log.info(f"Proactive notification sent: type={notif_type}, to={payload.phone}")
    return {"status": "sent", "to": payload.phone, "type": notif_type}


@app.post("/api/v1/whatsapp-webhook")
@limiter.limit("60/minute")
async def whatsapp_webhook_v1(
    request: Request,
    background_tasks: BackgroundTasks,
    Body: str = Form(""),
    From: str = Form(""),
    To: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None),
):
    """Twilio WhatsApp Webhook (versioned)."""
    if settings.validate_twilio_signature:
        signature = request.headers.get("X-Twilio-Signature", "")
        form_data = dict(await request.form())
        webhook_url = f"{settings.webhook_base_url}/api/v1/whatsapp-webhook"

        if not verify_twilio_signature(webhook_url, form_data, signature):
            log.warning(f"Rejected invalid Twilio signature from {From}")
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    twiml_response = MessagingResponse()
    background_tasks.add_task(
        handle_message_task, From, To, Body, NumMedia, MediaUrl0, MediaContentType0
    )
    return PlainTextResponse(str(twiml_response), media_type="text/xml")


# Backward-compatible unversioned route
@app.post("/whatsapp-webhook")
@limiter.limit("60/minute")
async def whatsapp_webhook_legacy(
    request: Request,
    background_tasks: BackgroundTasks,
    Body: str = Form(""),
    From: str = Form(""),
    To: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None),
):
    """Legacy unversioned webhook — forwards to v1."""
    return await whatsapp_webhook_v1(
        request, background_tasks, Body, From, To, NumMedia, MediaUrl0, MediaContentType0
    )
