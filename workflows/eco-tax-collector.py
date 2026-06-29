"""Eco-tax collection workflow.
Scheduled cron job that collects and records eco-tax for each active reservation.
Produces an auditable trail for regulatory compliance.
"""

import httpx
import logging
from datetime import date
from typing import List, Dict

logger = logging.getLogger(__name__)

ECO_TAX_RATE = 0.50  # per person per night


class EcoTaxCollector:
    def __init__(self, api_token: str, base_url: str):
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.base_url = base_url

    async def get_active_reservations(self, check_date: date) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/reservations/active",
                headers=self.headers,
                params={"date": check_date.isoformat()},
            )
            response.raise_for_status()
            return response.json().get("reservations", [])

    def calculate_tax(self, guests: int, nights: int) -> float:
        return round(guests * nights * ECO_TAX_RATE, 2)

    async def record_tax(self, reservation_id: str, amount: float) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/eco-tax",
                headers=self.headers,
                json={
                    "reservation_id": reservation_id,
                    "amount": amount,
                    "collected_at": date.today().isoformat(),
                },
            )
            response.raise_for_status()
            return response.json()

    async def run(self, check_date: date) -> List[Dict]:
        reservations = await self.get_active_reservations(check_date)
        results = []
        for res in reservations:
            tax = self.calculate_tax(res.get("guests", 1), res.get("nights", 1))
            result = await self.record_tax(res["id"], tax)
            results.append(result)
            logger.info(f"Recorded eco-tax {tax} for reservation {res['id']}")
        return results
