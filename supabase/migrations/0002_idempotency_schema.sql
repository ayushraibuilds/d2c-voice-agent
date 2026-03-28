-- Adds idempotency tracking for incoming Twilio webhooks

CREATE TABLE public.processed_messages (
    message_sid TEXT PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Index for quick cleanup of old entries
CREATE INDEX idx_processed_messages_created_at ON public.processed_messages(created_at);
