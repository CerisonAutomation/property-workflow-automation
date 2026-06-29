# Property Workflow Automation

**Property ops automation** — booking reconciliation, eco-tax collection, reservation-driven gate access control, automated guest communications, and secure HMAC-verified webhook workflows. Built for Christiano Vincenti Property Management, Malta.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi)]()
[![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen?style=flat)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat)]()

---

## Structure

```
property-workflow-automation/
├── workflows/
│   ├── booking_reconciliation.py   # Poll + diff bookings across two sources
│   ├── eco_tax_collector.py        # Malta eco-tax calculation and collection
│   ├── access_control.py           # Reservation-driven gate access provisioning
│   ├── guest_comms.py              # Confirmation, check-in instructions, reminders
│   └── webhook_handler.py          # FastAPI router — event dispatcher with decorator registry
├── security/
│   └── webhook_verification.py     # HMAC-SHA256 signature verification
├── tests/
│   ├── test_booking_reconciliation.py
│   ├── test_access_control.py
│   └── test_webhook_verification.py
├── app.py                          # FastAPI entry point
├── requirements.txt
├── Makefile
└── .env.example
```

---

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env
make dev
# API available at http://localhost:8001
```

---

## Run tests

```bash
make test
# or
pytest tests/ -v
```

---

## Webhook events handled

| Event | Action |
|---|---|
| `reservation.created` | Send confirmation email + provision gate access code |
| `reservation.cancelled` | Revoke gate access code |
| `reservation.modified` | Update access code window |

All webhook requests are HMAC-SHA256 verified before processing.

---

## Built by

> [Cerison Brown](https://github.com/CerisonAutomation) — Automation Engineer specialising in property ops platforms, secure webhook integrations, and production Python workflow systems.
