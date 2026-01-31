"""Entry point — start the Telegram bot with polling."""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import config
from handlers import on_text, on_non_text, on_clear
from logger import log


def main() -> None:
    config.validate()

    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("clear", on_clear))

    # Text messages from any chat (groups, supergroups, channels, private)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.UpdateType.CHANNEL_POST, on_text))

    # Non-text — log and ignore
    non_text = (
        filters.VOICE | filters.VIDEO_NOTE | filters.PHOTO | filters.VIDEO
        | filters.Sticker.ALL | filters.Document.ALL | filters.AUDIO | filters.ANIMATION
    )
    app.add_handler(MessageHandler(non_text, on_non_text))
    app.add_handler(MessageHandler(non_text & filters.UpdateType.CHANNEL_POST, on_non_text))

    bot_info = app.bot
    log("STARTUP", f"bot starting, polling...")

    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=["message", "channel_post"],
    )


if __name__ == "__main__":
    main()
