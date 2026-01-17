# Market Commentary Assistant (Investment Coach Bot)

An interactive **chat-based assistant** that helps users **learn investing concepts** and get **neutral market commentary** — while strictly **avoiding buy/sell recommendations or personalized investment advice**.

This project was built as a **safe, compliance-first GenAI prototype**, focusing on guardrails, conversation flow, and clean system design rather than predictions or tips.

---

## 🚀 What This Assistant Does

### 1. Investment Coach Mode (Teacher Persona)
- Explains investing concepts from **Beginner → Intermediate**
- Topics include: ETFs, SIPs, risk, diversification, valuation basics
- Uses **simple language and analogies**
- **Educational only** — no stock names, no recommendations

Example:
> "Explain ETFs in simple terms"

---

### 2. Market Commentary Mode (News Persona)
- Responds to queries like:
  - "Why is the market down today?"
  - "Summarize today’s market news"
- Provides **neutral, news-style summaries**
- Focuses on macro factors such as:
  - Inflation
  - Interest rates
  - Earnings trends
  - Global / geopolitical cues

Example:
> "Why is the market down today?"

---

### 3. Safety & Compliance Guardrails (Critical)
- **Refuses** all requests for:
  - Stock picks
  - Buy/sell calls
  - Intraday tips
  - Guaranteed returns
  - Personalized investment advice
- Always includes a **clear disclaimer**
- **Redirects users to education** instead of leaving them stuck

Example:
> "Which stock should I buy today?"

Response behavior:
- Clear refusal
- Educational alternative
- Disclaimer included

> *Educational purposes only — not investment advice.*

---

## 🧠 Design Philosophy

This project is **not** a trading bot or advisory system.

The core design goals are:
- Safety-first LLM usage
- Strong guardrails against misuse
- Clear separation of personas (Teacher vs Commentator)
- Simple, readable, modular code

---

## 🛠 Tech Stack

### Backend
- **Python**
- **FastAPI** (API + service layer)

### LLM
- **Groq API** (OpenAI-compatible)
- Model: `llama-3.1-8b-instant`
- Chosen for:
  - Low cost / free-tier friendliness
  - Fast inference
  - Open-source model support

### Interface
- **Telegram Bot** (long polling for development)

### Data
- **Mock market news data** (explicitly allowed for MVP)
- Modular data layer designed to be replaced with:
  - GDELT
  - Alpha Vantage News
  - Other free news APIs

### Infrastructure (Free-tier compatible)
- Designed for deployment on:
  - Render
  - Railway
  - Vercel (backend only)

---

## 📁 Project Structure

```
market-assistant/
│
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── telegram_bot.py    # Telegram bot (polling)
│   ├── router.py          # Intent / mode detection
│   ├── prompts.py         # System prompts (Coach / Commentary / Guardrail)
│   ├── llm.py             # Groq LLM wrapper
│   ├── news.py            # Mock market news data
│   └── safety.py          # Output safety enforcement
│
├── web/                   # (Optional) simple web UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ How to Run Locally

### 1. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 4. Run Telegram bot (polling mode)
```bash
python -m app.telegram_bot
```

Open Telegram and start chatting with your bot.

---

## 🧪 Sample Test Prompts

### Coach Mode
- Explain ETFs
- What is SIP?
- How does diversification reduce risk?

### Commentary Mode
- Why is the market down today?
- Summarize today’s market news

### Guardrail (Expected Refusal)
- Which stock should I buy today?
- Give me intraday tips
- Best stock for quick profit

---

## 🔒 Safety & Compliance Notes

- The assistant **never** provides:
  - Buy/sell recommendations
  - Stock picks
  - Price targets
  - Personalized advice
- Guardrails are enforced using:
  - Intent detection
  - System prompts
  - Post-generation safety checks

This ensures the system behaves as a **coach/commentator**, not an advisor.

---

## 🔮 Future Improvements (Optional)

- Replace mock news with live news APIs (GDELT / Alpha Vantage)
- Deploy Telegram bot using webhooks on Render
- Add conversation memory for learning progression
- Add structured learning paths (Beginner → Intermediate)

---

## ⚠️ Disclaimer

This project is for **educational purposes only** and does **not** constitute financial or investment advice. Investing involves risk, and users should perform their own research or consult a qualified professional before making financial decisions.

---

## 🙌 Acknowledgements

Built as part of an **Investment Coach + Market Commentary Assistant** take-home assignment, with a focus on safe, compliant GenAI system design.

