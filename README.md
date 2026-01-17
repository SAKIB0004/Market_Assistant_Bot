# Market Commentary Assistant – Telegram Bot

A **Telegram-based Investment Coach & Market Commentary Assistant** built with **FastAPI** and **Groq (OpenAI-compatible)**.

The assistant helps users:
- Learn investing concepts (Beginner → Intermediate)
- Get neutral, news-style market commentary

🚫 **Crucial constraint**: The bot **never** provides buy/sell recommendations, stock tips, intraday calls, or personalized investment advice. It acts strictly as a **coach/commentator**, not an advisor.

---

## ✨ Key Features

### 1. Investment Coach Mode
- Explains concepts like ETFs, SIPs, risk, diversification
- Uses simple language and analogies
- Educational only, no product or stock recommendations

### 2. Market Commentary Mode
- Answers questions like:
  - “Why is the market down today?”
  - “Summarize today’s market news”
- Neutral, journalist-style summaries
- Focus on macro, rates, earnings, global cues

### 3. Safety & Compliance Guardrails
- Refuses:
  - Stock picks
  - Buy/sell advice
  - Intraday tips
  - Guaranteed returns
- Always redirects users to **educational frameworks**
- Clear disclaimer included in relevant responses

---


## 🧠 System Design Overview

```
User (Telegram)
      ↓
Telegram Webhook
      ↓
FastAPI (Render)
      ↓
Mode Router (Coach / Commentary / Guardrail)
      ↓
Groq LLM
      ↓
Safe, compliant response
```

---

## 🛠 Tech Stack

### Backend
- **Python**
- **FastAPI** (API + service layer)

### LLM
- **Groq API** 
- Model: `llama-3.3-70b-versatile`
- Chosen for:
  - Low cost / free-tier friendliness
  - Fast inference
  - Open-source model support

### Interface
- **Telegram Bot** (Webhook mode)

### Data
- **Mock market news data** 

### Infrastructure (Free-tier compatible)
- Render

---

## 📁 Project Structure

```
project-root/
│
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── telegram_webhook.py   # Telegram webhook handler
│   ├── llm.py                # Groq client
│   ├── router.py             # Intent / mode detection
│   ├── prompts.py            # System prompts
│   ├── news.py               # Mock market news
│   └── safety.py             # Output safety enforcement
│
├── requirements.txt
├── .env.example
└── README.md
```

---


## ⚙️ Local Setup Instructions

### 1. Prerequisites
- Python **3.11+**
- A **Groq API key**
- A **Telegram Bot Token** (via @BotFather)

---

### 2. Clone the Repository

```bash
git clone  https://github.com/SAKIB0004/Market_Assistant_Bot.git
cd Market_Assistant_Bot
```

---

### 3. Create & Activate Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY="groq_api_key"
GROQ_MODEL=llama-3.3-70b-versatile
TELEGRAM_BOT_TOKEN="telegram_bot_token"
```

---

### 6. Run Locally (Webhook-style API)

```bash
uvicorn app.main:app --reload
```

---

## 🚀 Deployment on Render (Telegram Webhook)

### 1. Create a Render Web Service

- Environment: **Python**
- Build Command:
  ```bash
  pip install -r requirements.txt
  ```
- Start Command:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

---

## Render URL:

```
https://market-assistant-bot.onrender.com
```

## Using the Telegram Bot

The bot is deployed and available on Telegram.

### How to Find the Bot
1. Open **Telegram**
2. Search for the bot by username: `Market_Commentary_Assistant_Bot`

or 

🔗 **Live Telegram Bot**: https://t.me/Market_Commentary_Assistant_Bot

### Start the Bot
1. Open the chat
2. Click **Start**
3. Send a message (no commands required)

---

## 🧪 Example Test Prompts

### Coach Mode
- Explain ETFs
- What is SIP?
- How does diversification reduce risk?

### Commentary Mode
- Why is the market down today?
- Summarize today’s market news

### Guardrail Test
- Which stock should I buy today?
- Give me intraday tips

(Expected: refusal + educational redirection)

---

## 🔒 Compliance & Safety Notes

- No stock recommendations
- No buy/sell language
- No personalized advice
- Explicit refusal + redirection logic

This ensures the assistant remains a **coach/commentator**, not an investment advisor.


## ⚠️ Disclaimer

This project is for **educational purposes only** and does **not** constitute financial or investment advice. Investing involves risk, and users should perform their own research or consult a qualified professional before making financial decisions.

---

## 🙌 Acknowledgements

Built as part of an **Investment Coach + Market Commentary Assistant** take-home assignment, with a focus on safe, compliant GenAI system design.

