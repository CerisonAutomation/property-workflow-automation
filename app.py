"""Property Workflow Automation — FastAPI entry point.
Exposes webhook endpoints and workflow triggers.
"""

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
import logging
import os

from security.webhook_verification import verify_guesty_signature
from workflows.booking_reconciliation import BookingReconciler
from workflows.eco_tax_collector import EcoTaxCollector
from workflows.access_control import AccessController
from workflows.guest_comms import GuestComms

logger = logging.getLogger(__name__)
app = FastAPI(title="Property Workflow Automation", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhooks/guesty")
async def guesty_webhook(
    request: Request,
    x_guesty_signature: str = Header(None),
):
    body = await request.body()
    secret = os.environ["WEBHOOK_SECRET"]

    if not verify_guesty_signature(body, x_guesty_signature, secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event_type = payload.get("event")
    logger.info(f"Received Guesty event: {event_type}")

    if event_type == "reservation.created":
        comms = GuestComms()
        await comms.send_confirmation(payload["data"])
        ctrl = AccessController(os.environ["ACCESS_GATE_CALLBACK_URL"])
        await ctrl.provision_access(payload["data"])

    return JSONResponse({"received": True})


@app.post("/workflows/reconcile")
async def run_reconciliation():
    reconciler = BookingReconciler(
        api_token=os.environ["GUESTY_CLIENT_ID"],
        base_url=os.environ["GUESTY_API_BASE"],
    )
    from datetime import datetime, timedelta
    result = await reconciler.reconcile(
        source_bookings=[],
        target_bookings=[],
    )
    return result
