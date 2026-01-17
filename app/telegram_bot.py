import os
import logging
import re
from dotenv import load_dotenv

# MUST be first so env vars exist before other imports
load_dotenv()

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Import your existing backend logic (re-use!)
from app.router import detect_mode
from app.prompts import COACH_SYSTEM, COMMENTARY_SYSTEM, GUARDRAIL_SYSTEM
from app.news import get_todays_items
from app.llm import generate
from app.safety import enforce_output_safety

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# -------------------------
# Logging: redaction + less noise
# -------------------------

class RedactBotTokenFilter(logging.Filter):
    """
    Redacts Telegram bot token patterns from any log record message.
    Telegram API URLs often contain: https://api.telegram.org/bot<token>/...
    """
    def __init__(self, token: str | None):
        super().__init__()
        self.token = token

        # Common Telegram token pattern: "<digits>:<letters_numbers_-...>"
        self.generic_token_pattern = re.compile(r"\b\d{6,}:[A-Za-z0-9_-]{20,}\b")

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()

            # Redact the exact token if we know it
            if self.token and self.token in msg:
                msg = msg.replace(self.token, "[REDACTED_TELEGRAM_TOKEN]")

            # Redact any token-looking substrings (defense-in-depth)
            msg = self.generic_token_pattern.sub("[REDACTED_TELEGRAM_TOKEN]", msg)

            # Also redact "bot<token>" inside URLs
            msg = re.sub(r"bot\[REDACTED_TELEGRAM_TOKEN\]", "bot[REDACTED_TELEGRAM_TOKEN]", msg)

            record.msg = msg
            record.args = ()
        except Exception:
            # Never break logging
            pass
        return True


# Configure root logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Reduce noisy third-party logs that tend to include request URLs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.INFO)  # keep app-level info

# Add redaction filter to all handlers
_root = logging.getLogger()
for h in _root.handlers:
    h.addFilter(RedactBotTokenFilter(TOKEN))

logger = logging.getLogger("telegram_bot")


HELP_TEXT = (
    "Hi! I can:\n"
    "1) Teach investing concepts (beginner → intermediate)\n"
    "2) Provide neutral market commentary\n\n"
    "Try:\n"
    "- Explain ETFs\n"
    "- What is SIP?\n"
    "- Why is the market down today?\n\n"
    "Note: Educational purposes only — not investment advice."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong ✅")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            return

        user_text = (update.message.text or "").strip()
        logger.info(
            "INCOMING from %s: %s",
            update.effective_user.id if update.effective_user else "unknown",
            user_text,
        )

        if not user_text:
            await update.message.reply_text("Send a text message and I’ll respond.")
            return

        await update.message.chat.send_action(action=ChatAction.TYPING)

        mode = detect_mode(user_text)

        if mode == "GUARDRAIL":
            text = generate(GUARDRAIL_SYSTEM, user_text)
            text = enforce_output_safety(text)
            await update.message.reply_text(text)
            return

        if mode == "COMMENTARY":
            news = get_todays_items()
            prompt = (
                f"User asked: {user_text}\n\n"
                f"Use these news items (as_of={news['as_of']}):\n"
                + "\n".join(
                    [
                        f"- [{x['category']}] {x['headline']} (source: {x['source']})"
                        for x in news["items"]
                    ]
                )
                + "\n\nWrite a neutral market wrap in 6-10 bullets + 2-line summary. End with disclaimer."
            )
            text = generate(COMMENTARY_SYSTEM, prompt)
            text = enforce_output_safety(text)
            await update.message.reply_text(text)
            return

        # COACH
        text = generate(COACH_SYSTEM, user_text)
        text = enforce_output_safety(text)
        await update.message.reply_text(text)

    except Exception as e:
        logger.exception("Handler error: %s", e)
        if update.message:
            await update.message.reply_text(
                "Sorry — I hit an internal error while generating the response.\n"
                "Please try again. If it keeps happening, check the bot logs."
            )


async def on_startup(app: Application):
    logger.info("Bot starting up...")
    try:
        await app.bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook cleared (if one existed).")
    except Exception as e:
        logger.warning("Could not clear webhook: %s", e)


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing. Put it in your .env file.")

    application = (
        Application.builder()
        .token(TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.post_init = on_startup

    logger.info("Running bot with long polling...")
    application.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
