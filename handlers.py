"""Telegram bot message handlers."""

from telegram import Update
from telegram.ext import ContextTypes

import buffer_client
from formatter import format_message
from logger import log


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages — format and send to buffer."""
    msg = update.message or update.channel_post
    if msg is None or msg.text is None:
        return

    formatted = format_message(msg)
    log("MESSAGE", formatted)
    buffer_client.send(formatted)


async def on_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command — reset Claude session."""
    msg = update.message
    if msg is None:
        return

    user = msg.from_user
    who = f"@{user.username}" if user and user.username else f"@{user.id}" if user else "@unknown"
    log("COMMAND", f"/clear from {who} in chat {msg.chat_id}")

    if buffer_client.clear_session():
        await msg.reply_text("Session cleared.")
    else:
        await msg.reply_text("Failed to clear session.")


async def on_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log and ignore non-text messages (voice, photo, sticker, etc.)."""
    msg = update.message or update.channel_post
    if msg is None:
        return

    # Determine type for logging
    for attr in ("voice", "video_note", "photo", "video", "sticker", "document", "audio", "animation"):
        if getattr(msg, attr, None):
            user = msg.from_user
            who = f"@{user.username}" if user and user.username else f"@{user.id}" if user else "@unknown"
            log("IGNORED", f"{attr} message from {who} in chat {msg.chat_id}")
            return
