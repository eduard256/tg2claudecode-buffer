"""HTTP client for sending messages to claudecode2api-buffer."""

import httpx

import config
from logger import log


# Single reusable client — created once, lives forever.
_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    """Lazy-init a persistent httpx client with basic auth."""
    global _client
    if _client is None:
        _client = httpx.Client(
            base_url=config.BUFFER_URL,
            auth=(config.BUFFER_USER, config.BUFFER_PASS),
            timeout=10.0,
        )
    return _client


def send(text: str) -> bool:
    """Send a message to the buffer. Returns True on success, False on error."""
    try:
        r = _get_client().post("/v1/message", json={"text": text})
        if r.status_code == 200:
            log("SENT", "ok")
            return True
        log("ERROR", f"buffer returned {r.status_code}: {r.text}")
        return False
    except Exception as e:
        log("ERROR", f"buffer unavailable: {e}")
        return False


def clear_session() -> bool:
    """Reset Claude session via DELETE /v1/session. Returns True on success."""
    try:
        r = _get_client().delete("/v1/session")
        if r.status_code == 200:
            log("SESSION", "cleared")
            return True
        log("ERROR", f"session clear returned {r.status_code}: {r.text}")
        return False
    except Exception as e:
        log("ERROR", f"buffer unavailable: {e}")
        return False
