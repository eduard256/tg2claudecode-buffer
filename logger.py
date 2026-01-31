"""Simple stdout logger with timestamps."""

from datetime import datetime, timezone


def log(tag: str, message: str) -> None:
    """Print a timestamped log line to stdout."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {tag}: {message}", flush=True)
