"""Booking reconciliation workflow.
Polls booking API, matches records, and flags discrepancies.
Production-deployed for Christiano Property Management, Malta.
"""

import httpx
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class BookingReconciler:
    def __init__(self, api_token: str, base_url: str):
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.base_url = base_url

    async def fetch_bookings(self, from_date: datetime, to_date: datetime) -> list:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/bookings",
                headers=self.headers,
                params={
                    "from": from_date.isoformat(),
                    "to": to_date.isoformat(),
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("data", [])

    async def reconcile(self, source_bookings: list, target_bookings: list) -> dict:
        source_ids = {b["id"] for b in source_bookings}
        target_ids = {b["id"] for b in target_bookings}

        missing = source_ids - target_ids
        extra = target_ids - source_ids

        logger.info(f"Reconciliation: {len(missing)} missing, {len(extra)} extra")

        return {
            "matched": len(source_ids & target_ids),
            "missing_in_target": list(missing),
            "extra_in_target": list(extra),
            "timestamp": datetime.utcnow().isoformat(),
        }
