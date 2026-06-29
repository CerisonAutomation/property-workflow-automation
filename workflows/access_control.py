"""
Reservation-driven access control.
On reservation creation/cancellation, provisions or revokes gate access codes.
Production-deployed for Nine Angels Villa, Madliena, Malta.
"""

import httpx
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AccessController:
    def __init__(self, gate_callback_url: str):
        self.gate_callback_url = gate_callback_url

    def _generate_code(self, reservation_id: str, checkin: str) -> str:
        """Deterministic 6-digit access code from reservation ID + checkin date."""
        import hashlib
        raw = f"{reservation_id}:{checkin}"
        digest = hashlib.sha256(raw.encode()).hexdigest()
        return str(int(digest[:8], 16) % 900_000 + 100_000)

    async def provision_access(self, reservation: dict) -> dict:
        """Create a time-limited access code for the reservation window."""
        code = self._generate_code(
            reservation["_id"],
            reservation.get("checkIn", ""),
        )
        payload = {
            "action": "provision",
            "reservation_id": reservation["_id"],
            "code": code,
            "valid_from": reservation.get("checkIn"),
            "valid_until": reservation.get("checkOut"),
            "guest_name": reservation.get("guest", {}).get("fullName", ""),
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.gate_callback_url,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
        logger.info(f"Access provisioned for reservation {reservation['_id']}")
        return {"code": code, "status": "provisioned"}

    async def revoke_access(self, reservation_id: str) -> dict:
        """Revoke access code on cancellation or early checkout."""
        payload = {"action": "revoke", "reservation_id": reservation_id}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.gate_callback_url,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
        logger.info(f"Access revoked for reservation {reservation_id}")
        return {"status": "revoked"}
