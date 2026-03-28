# D2C Voice Agent RUNBOOK

This runbook outlines the operational procedures for deploying, managing, and debugging the D2C Voice-First Agent backend.

## 1. Required Secrets & Validations
The application utilizes a `startup_checks()` routine during the FastAPI `lifespan` event. If any of the following environment variables are missing, the container will instantly crash with an exit code of `1`:

- `TWILIO_ACCOUNT_SID`: Mandatory. Your Twilio account SID.
- `TWILIO_AUTH_TOKEN`: Mandatory. Used to sign requests and download media.
- `GROQ_API_KEY`: Mandatory. Required for LLM routing and Whisper ingestion.
- `SUPABASE_URL` & `SUPABASE_SERVICE_KEY`: Highly recommended. Must be configured or the bot cannot manage ecommerce history dynamically.

## 2. Twilio Signature Verification
Twilio authenticates against `/api/v1/whatsapp-webhook` by signing incoming requests using your `TWILIO_AUTH_TOKEN`.
If requests are rejected with a `403 Invalid Twilio signature`, verify:
1. `WEBHOOK_BASE_URL` in your `.env` perfectly matches the URL configured in the Twilio dashboard (including `https://` and without a trailing slash).
2. You have not accidentally rotated your Twilio Auth Token.

## 3. Webhook Idempotency & Retries
Twilio aggressively retries webhook delivery if the backend fails to respond within 15 seconds.
- The system prevents duplicate agent actions by checking the `processed_messages` table matching the Twilio `MessageSid`.
- If an agent task takes longer than 15s to complete, Twilio will re-transmit the POST. The application will see the `MessageSid` exists inside `processed_messages` and return an immediate HTTP 200 without executing the background task twice.

## 4. Diagnostics & Logging
- **Voice Ingestion**: If users send voice notes that fail to transcribe, check the logs for GROQ timeout errors. The system automatically retries downloading standard `.ogg` payloads from Twilio 3 times.
- **Deduplication Check**: Run `SELECT * FROM processed_messages ORDER BY created_at DESC LIMIT 10;` via Supabase to ensure incoming webhooks are successfully recorded.
