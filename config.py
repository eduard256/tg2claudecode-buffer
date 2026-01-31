"""Configuration loaded from environment variables."""

import os
import sys


TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BUFFER_URL: str = os.environ.get("BUFFER_URL", "http://localhost:3856")
BUFFER_USER: str = os.environ.get("BUFFER_USER", "")
BUFFER_PASS: str = os.environ.get("BUFFER_PASS", "")


def validate() -> None:
    """Exit immediately if required env vars are missing."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not BUFFER_USER:
        missing.append("BUFFER_USER")
    if not BUFFER_PASS:
        missing.append("BUFFER_PASS")
    if missing:
        print(f"FATAL: missing env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
