from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.router import detect_mode
from app.prompts import COACH_SYSTEM, COMMENTARY_SYSTEM, GUARDRAIL_SYSTEM
from app.news import get_todays_items
from app.llm import generate
from app.safety import enforce_output_safety
from app.telegram_webhook import router as telegram_router

app = FastAPI(title="Market Commentary Assistant")
app.include_router(telegram_router)

class ChatIn(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
def chat(payload: ChatIn):
    user_text = payload.message
    mode = detect_mode(user_text)

    if mode == "GUARDRAIL":
        text = generate(GUARDRAIL_SYSTEM, user_text)
        return {"mode": mode, "response": enforce_output_safety(text)}

    if mode == "COMMENTARY":
        news = get_todays_items()
        prompt = (
            f"User asked: {user_text}\n\n"
            f"Use these news items (as_of={news['as_of']}):\n"
            + "\n".join([f"- [{x['category']}] {x['headline']} (source: {x['source']})" for x in news["items"]])
            + "\n\nWrite a neutral market wrap in 6-10 bullets + 2-line summary. End with disclaimer."
        )
        text = generate(COMMENTARY_SYSTEM, prompt)
        return {"mode": mode, "response": enforce_output_safety(text)}

    # COACH
    text = generate(COACH_SYSTEM, user_text)
    return {"mode": mode, "response": enforce_output_safety(text)}
