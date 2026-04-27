from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters
)

from bot.handlers import handle_message, handle_start, handle_help
from app.config import settings


def create_bot():
    """
    Build and configure the Telegram bot application.
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is not set. "
            "Check your .env file."
        )

    app = ApplicationBuilder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    # Command handlers
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help", handle_help))

    # Text message handler (natural language)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    return app