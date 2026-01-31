"""Format incoming Telegram messages for the buffer API."""

from telegram import Message


def format_message(msg: Message) -> str:
    """Build the formatted string: [msg:{id}] [chat:{chat_id}] @{user}: {text}"""
    user = msg.from_user
    if user and user.username:
        who = f"@{user.username}"
    elif user:
        who = f"@{user.id}"
    else:
        who = "@unknown"

    return f"[msg:{msg.message_id}] [chat:{msg.chat_id}] {who}: {msg.text}"
