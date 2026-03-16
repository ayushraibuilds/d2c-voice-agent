# D2C Voice-First AI Agent 🎙️

An enterprise-grade, voice-first WhatsApp AI Support Agent built specifically for Indian Direct-to-Consumer (D2C) brands. This monorepo contains the high-performance Python LangGraph backend and the modern Next.js B2B marketing landing page.

![Tech Stack](https://img.shields.io/badge/Stack-Next.js%20|%20FastAPI%20|%20LangGraph%20|%20Groq%20|%20Twilio-indigo)

---

## 🌟 Vision

Indian D2C brands face a unique customer support challenge: the dominance of WhatsApp and the prevalence of voice notes in regional languages or "Hinglish." Traditional chatbots fail entirely when confronted with a 10-second voice note asking "Mera refund kahan hai?" 

**Our Vision:** To provide Tier-2/3 customer support teams with an autonomous AI agent that seamlessly transcribes voice notes, classifies complex mixed-language intents, and integrates deeply with existing e-commerce backends (like ONDC and Shopify) to resolve tickets instantly.

---

## 🎯 Supported Intents (10)

| Intent | Description |
|--------|-------------|
| `ORDER_STATUS` | Track order delivery status |
| `REFUND_REQUEST` | Initiate a refund |
| `ORDER_CANCEL` | Cancel an active order |
| `EXCHANGE_REQUEST` | Exchange/replace a product |
| `PAYMENT_ISSUE` | Payment failures, double charges |
| `DELIVERY_COMPLAINT` | Late delivery, damaged goods |
| `PRODUCT_FAQ` | Return policy, shipping time, contact info |
| `HUMAN_HANDOFF` | Transfer to human agent with ticket |
| `GREETING` | Hi, Hello, Namaste |
| `UNKNOWN` | Fallback with helpful suggestions |

---

## 🏗️ Architecture

```
WhatsApp → Twilio → webhook.py (rate limit + signature validation)
                        │
                        ├── Audio? → Groq Whisper (with retries) → Text
                        │
                        └── support_graph.py (LangGraph)
                              │
                              ├── detect_language (hybrid 3-step)
                              ├── load_context (conversation memory)
                              ├── classify_intent (Groq LLM + sanitization)
                              └── action_node → ecommerce_adapter.py → database.py (SQLite)
                                                                        ├── Orders
                                                                        ├── Conversations
                                                                        └── Tickets
```

---

## 💻 Tech Stack

### Backend (`/backend`)
- **Framework:** FastAPI + Uvicorn (with CORS, rate limiting)
- **AI Orchestration:** LangGraph + LangChain Core
- **Inference:** Groq (`llama3-70b-8192` + `whisper-large-v3`)
- **Communication:** Twilio Messaging API (signature validation)
- **Database:** SQLite (orders, conversations, tickets)
- **Config:** Pydantic BaseSettings
- **Logging:** Structured logging with correlation IDs

### Frontend (`/frontend`)
- **Framework:** Next.js 16 (App Router, standalone output)
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Icons:** Lucide React

---

## 📂 Repository Structure

```text
d2c-voice-agent/
│
├── backend/                     # AI Execution Engine
│   ├── webhook.py               # FastAPI + Twilio webhook + API v1 endpoints
│   ├── support_graph.py         # LangGraph state machine (10 intents)
│   ├── database.py              # SQLite persistence layer
│   ├── ecommerce_adapter.py     # Abstract adapter (DB/ONDC/Shopify)
│   ├── config.py                # Pydantic BaseSettings singleton
│   ├── logger.py                # Structured logging + correlation IDs
│   ├── lang_detect.py           # Hybrid language classifier
│   ├── reply_templates.py       # Bilingual templates (EN + HI)
│   ├── requirements.txt         # Pinned Python dependencies
│   ├── Dockerfile               # Production container
│   └── .env.example             # Environment variables template
│
├── frontend/                    # B2B SaaS Marketing Landing Page
│   ├── src/app/                 # Next.js Pages & Layout
│   ├── src/components/          # 8 React UI Components
│   ├── Dockerfile               # Production container
│   └── package.json             # Node dependencies
│
├── docker-compose.yml           # Full stack orchestration
└── .github/workflows/ci.yml    # CI/CD pipeline
```

---

## 🚀 Getting Started

### 1. Backend Setup
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Fill in your keys
uvicorn webhook:app --reload --port 8000
```
The SQLite database auto-creates on first start.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:3000`.

### 3. Docker (Full Stack)
```bash
cp backend/.env.example backend/.env  # Fill in your keys
docker compose up --build
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/whatsapp-webhook` | Twilio webhook (rate limited) |
| `GET` | `/api/v1/conversations/{phone}` | Conversation history |
| `GET` | `/api/v1/tickets` | Open support tickets |
| `GET` | `/api/v1/stats` | Agent statistics |

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
