# Property Workflow Automation

**Production property operations automation** built for Christiano Property Management, Malta. Automates booking reconciliation, guest communication, eco-tax collection, reservation-driven access control, and admin workflows.

[![Google Apps Script](https://img.shields.io/badge/Google%20Apps%20Script-enabled-4285F4?style=flat&logo=google)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?style=flat&logo=fastapi)]()
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat)]()

---

## What it automates

| Workflow | How |
|---|---|
| Booking reconciliation | API polling + Google Apps Script |
| Guest communication | Event-driven webhook flows |
| Eco-tax collection | Scheduled cron + audit trail |
| Transfer handling | Reservation event triggers |
| Property access control | Reservation-driven token generation |
| Admin inbox management | Automated triage and follow-up |

---

## Architecture

```
Triggers        Webhooks · Cron jobs · API polling · Reservation events
Processing      Google Apps Script · FastAPI · Python
Security        OAuth 2.0 · JWT · HMAC-SHA256 · Token management
Reliability     Idempotency · Schema validation · Retry logic · Audit trails
Storage         PostgreSQL · Supabase · Redis-backed state
```

---

## Key outcomes

- Removed repeated admin work across inbox, reservations, and operational follow-up
- Stable and auditable workflows with idempotent request handling
- Reservation-driven access control with token-based security
- Production-deployed for live property operations in Malta

---

## Security patterns used

```python
# HMAC-SHA256 webhook verification
import hmac, hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

---

## Idempotency pattern

```python
# Idempotent request handler — prevents duplicate processing
async def process_event(event_id: str, payload: dict):
    if await redis.exists(f"processed:{event_id}"):
        return {"status": "already_processed"}
    await redis.setex(f"processed:{event_id}", 86400, "1")
    return await handle_payload(payload)
```

---

## Built by

> [Cerison Brown](https://github.com/CerisonAutomation) — Automation Engineer specialising in property ops automation, secure API integrations, and production workflow engineering.
