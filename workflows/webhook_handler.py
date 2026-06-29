"""
Webhook handler for Guesty events.
Verifies HMAC signature, routes to correct workflow.
"""

import logging
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
import os

from security.webhook_verification import verify_guesty_signature

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])

EVENT_HANDLERS = {}


def on_event(event_type: str):
    """Decorator to register a handler for a Guesty event type."""
    def decorator(fn):
        EVENT_HANDLERS[event_type] = fn
        return fn
    return decorator


@router.post("/guesty")
async def guesty_webhook(
    request: Request,
    x_guesty_signature: str = Header(None),
):
    body = await request.body()
    secret = os.environ.get("WEBHOOK_SECRET", "")

    if secret and not verify_guesty_signature(body, x_guesty_signature or "", secret):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event_type = payload.get("event")
    handler = EVENT_HANDLERS.get(event_type)

    if handler:
        logger.info(f"Handling event: {event_type}")
        await handler(payload.get("data", {}))
    else:
        logger.info(f"No handler registered for event: {event_type}")

    return JSONResponse({"received": True, "event": event_type})
