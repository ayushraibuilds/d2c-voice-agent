# D2C Voice-First AI Agent 🎙️

An enterprise-grade, voice-first WhatsApp AI Support Agent built specifically for Indian Direct-to-Consumer (D2C) brands. This monorepo contains the high-performance Python LangGraph backend and the modern Next.js B2B marketing landing page.

![Tech Stack](https://img.shields.io/badge/Stack-Next.js%20|%20FastAPI%20|%20LangGraph%20|%20Groq%20|%20Twilio-indigo)

---

## 🌟 Vision

Indian D2C brands face a unique customer support challenge: the dominance of WhatsApp and the prevalence of voice notes in regional languages or "Hinglish." Traditional chatbots fail entirely when confronted with a 10-second voice note asking "Mera refund kahan hai?" 

**Our Vision:** To provide Tier-2/3 customer support teams with an autonomous AI agent that seamlessly transcribes blisteringly fast voice notes, classifies complex mixed-language intents, and integrates deeply with existing e-commerce backends (like ONDC and Shopify) to resolve tickets instantly—all without human intervention unless absolutely necessary.

---

## 🎯 Use Cases

1. **Order Tracking via Voice:**
   - *Customer:* (Sends Voice Note) "Bhaiya mera joote ka order kab aayega?" (Brother, when will my shoe order arrive?)
   - *Agent:* Instantly transcribes, queries the e-commerce database, and replies: "📦 आपका ऑडर ORD-11223 अभी 'Out for Delivery' है। इसके आज रात 8 बजे तक पहुंचने की उम्मीद है।"
2. **Refund Initiation & Checking:**
   - *Customer:* "I want to cancel and get my paise wapas."
   - *Agent:* Checks eligibility against the database and automatically triggers the refund API.
3. **Product FAQs:**
   - Automates responses for return policies, shipping times, and general catalog queries.
4. **Smart Human Handoff (Zendesk/Freshdesk Stub):**
   - If a customer is frustrated or asks for a human, the AI creates an enterprise support ticket and hands off the conversation context smoothly.

---

## 🏗️ Product Architecture

The system is designed around a decoupled, API-first architecture:

### 1. The Twilio Webhook Layer
- Receives incoming WhatsApp payloads.
- **Media Interception:** Detects `OGG` audio payloads and securely downloads them using Twilio Auth.

### 2. The Audio Transcription Layer (Groq)
- Pushes the audio to **Groq's `whisper-large-v3`** model.
- Why Groq? It provides LPU-accelerated, near-instantaneous transcription, ensuring the WhatsApp user doesn't experience "chatbot lag."

### 3. The LangGraph State Machine
- **Node 1 (Language Detection):** A hybrid heuristic engine checking for Hinglish/Indic triggers or falling back to `langdetect`.
- **Node 2 (Intent Classifier):** Calls `llama3-70b-8192` with strict structured outputs to classify the prompt into one of five paths: `ORDER_STATUS`, `REFUND_REQUEST`, `PRODUCT_FAQ`, `HUMAN_HANDOFF`, or `UNKNOWN`. Also extracts entities like `order_id`.
- **Action Nodes:** Specific Python execution paths that interact with the Mock E-commerce Database or trigger the Zendesk Ticket Stub.

### 4. Localization Engine
- Replies are dynamically generated using `reply_templates.py`, which supports multi-language contextual responses (currently optimized for English and Hindi/Hinglish).

---

## 💻 Tech Stack

### Backend (`/backend`)
- **Framework Development:** FastAPI & Uvicorn
- **AI / LLM Orchestration:** LangGraph & LangChain Core
- **Inference & Transcription:** Groq (`llama3-70b-8192` & `whisper-large-v3`)
- **Communication:** Twilio Messaging API
- **Language Utilities:** `langdetect`, `indic-transliteration`

### Frontend (`/frontend`)
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Icons:** Lucide React

---

## 📂 Repository Structure

```text
d2c-voice-agent/
│
├── backend/                  # The AI Execution Engine
│   ├── webhook.py            # FastAPI entry point & Twilio handler
│   ├── support_graph.py      # LangGraph state machine & LLM Logic
│   ├── mock_ecommerce.py     # Stub database for testing orders
│   ├── lang_detect.py        # Hybrid custom language classifier
│   ├── reply_templates.py    # Localized dialogue templates
│   └── requirements.txt      # Python dependencies
│
└── frontend/                 # B2B SaaS Marketing Landing Page
    ├── src/app/              # Next.js Pages & Layout
    ├── src/components/       # React UI Components (Hero, InteractiveChat)
    ├── tailwind.config.ts    # Styling Configuration
    └── package.json          # Node dependencies
```

---

## 🚀 Getting Started

### 1. Setting up the Backend
Navigate to the `backend` directory and install dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
GROQ_API_KEY=your_groq_api_key
```

Run the server:
```bash
uvicorn webhook:app --reload --port 8000
```
*Use `ngrok http 8000` to expose this webhook to Twilio.*

### 2. Setting up the Frontend
Navigate to the `frontend` directory:
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:3000` to view the animated B2B landing page.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
