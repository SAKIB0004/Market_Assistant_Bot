import os
from fastapi import APIRouter, Request, HTTPException
from telegram import Update
from telegram.ext import Application

from app.router import detect_mode
from app.prompts import COACH_SYSTEM, COMMENTARY_SYSTEM, GUARDRAIL_SYSTEM
from app.news import get_todays_items
from app.llm import generate
from app.safety import enforce_output_safety

router = APIRouter()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    # FastAPI will still boot, but webhook will fail without token
    pass

# Build an in-memory telegram Application (no polling)
tg_app = Application.builder().token(TOKEN).build()


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    if not TOKEN:
        raise HTTPException(status_code=500, detail="TELEGRAM_BOT_TOKEN missing")

    payload = await request.json()

    update = Update.de_json(payload, tg_app.bot)

    # Only handle normal messages for MVP
    if not update.message or not update.message.text:
        return {"ok": True}

    user_text = update.message.text.strip()
    chat_id = update.message.chat_id

    mode = detect_mode(user_text)

    if mode == "GUARDRAIL":
        text = generate(GUARDRAIL_SYSTEM, user_text)
        text = enforce_output_safety(text)
        await tg_app.bot.send_message(chat_id=chat_id, text=text)
        return {"ok": True}

    if mode == "COMMENTARY":
        news = get_todays_items()
        prompt = (
            f"User asked: {user_text}\n\n"
            f"Use these news items (as_of={news['as_of']}):\n"
            + "\n".join([f"- [{x['category']}] {x['headline']} (source: {x['source']})" for x in news["items"]])
            + "\n\nWrite a neutral market wrap in 6-10 bullets + 2-line summary. End with disclaimer."
        )
        text = generate(COMMENTARY_SYSTEM, prompt)
        text = enforce_output_safety(text)
        await tg_app.bot.send_message(chat_id=chat_id, text=text)
        return {"ok": True}

    # COACH
    text = generate(COACH_SYSTEM, user_text)
    text = enforce_output_safety(text)
    await tg_app.bot.send_message(chat_id=chat_id, text=text)
    return {"ok": True}
