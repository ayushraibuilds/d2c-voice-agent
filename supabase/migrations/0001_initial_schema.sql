-- Initial schema for D2C Voice Agent

CREATE TABLE public.brands (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    api_key TEXT UNIQUE,
    whatsapp_number TEXT UNIQUE NOT NULL,
    custom_prompt TEXT DEFAULT '',
    webhook_url TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE public.products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    price NUMERIC NOT NULL,
    category TEXT DEFAULT '',
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Note: text_search index is implicitly supported via Supabase Postgres
ALTER TABLE public.products ADD COLUMN name_desc_search tsvector GENERATED ALWAYS AS (to_tsvector('english', name || ' ' || coalesce(description, ''))) STORED;
CREATE INDEX idx_products_search ON public.products USING GIN (name_desc_search);

CREATE TABLE public.customers (
    id SERIAL PRIMARY KEY,
    phone TEXT UNIQUE NOT NULL,
    name TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE public.orders (
    id SERIAL PRIMARY KEY,
    order_id TEXT UNIQUE NOT NULL,
    customer_phone TEXT NOT NULL REFERENCES public.customers(phone),
    status TEXT NOT NULL DEFAULT 'Processing',
    items JSONB NOT NULL DEFAULT '[]'::jsonb,
    estimated_delivery TEXT DEFAULT '',
    refund_status TEXT DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE public.conversations (
    id SERIAL PRIMARY KEY,
    phone TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
    message TEXT NOT NULL,
    intent TEXT DEFAULT '',
    detected_lang TEXT DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE public.tickets (
    id SERIAL PRIMARY KEY,
    ticket_id TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    message TEXT NOT NULL,
    intent TEXT DEFAULT '',
    image_url TEXT DEFAULT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    assigned_to TEXT DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indexes
CREATE INDEX idx_orders_phone ON public.orders(customer_phone);
CREATE INDEX idx_orders_order_id ON public.orders(order_id);
CREATE INDEX idx_conversations_phone ON public.conversations(phone);
CREATE INDEX idx_conversations_created_at ON public.conversations(created_at);
CREATE INDEX idx_tickets_status ON public.tickets(status);

-- Seed Data (Development)
INSERT INTO public.brands (name, api_key, whatsapp_number, custom_prompt) 
VALUES ('Acme D2C', 'dummy-api-key-123', '+14155238886', 'You are a highly professional and polite support agent for Acme D2C. Be concise and empathetic.')
ON CONFLICT DO NOTHING;

INSERT INTO public.customers (phone, name) VALUES ('+919876543210', 'Rahul Sharma') ON CONFLICT DO NOTHING;

INSERT INTO public.orders (order_id, customer_phone, status, items, estimated_delivery) 
VALUES ('ORD-12345', '+919876543210', 'Out for Delivery', '["Wireless Earbuds"]'::jsonb, 'Today by 8 PM')
ON CONFLICT DO NOTHING;

INSERT INTO public.products (name, description, price, category, stock) 
VALUES ('Bolt Smartwatch Pro', 'Premium waterproof smartwatch', 2999.0, 'Electronics', 150)
ON CONFLICT DO NOTHING;
