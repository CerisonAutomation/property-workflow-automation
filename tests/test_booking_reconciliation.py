"""Tests for booking reconciliation workflow."""
import pytest
from workflows.booking_reconciliation import BookingReconciler


@pytest.fixture
def reconciler():
    return BookingReconciler(api_token="test-token", base_url="https://api.example.com")


@pytest.mark.asyncio
async def test_reconcile_no_discrepancies(reconciler):
    bookings = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    result = await reconciler.reconcile(bookings, bookings)
    assert result["matched"] == 3
    assert result["missing_in_target"] == []
    assert result["extra_in_target"] == []


@pytest.mark.asyncio
async def test_reconcile_missing_in_target(reconciler):
    source = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    target = [{"id": "1"}, {"id": "2"}]
    result = await reconciler.reconcile(source, target)
    assert "3" in result["missing_in_target"]
    assert result["matched"] == 2


@pytest.mark.asyncio
async def test_reconcile_extra_in_target(reconciler):
    source = [{"id": "1"}]
    target = [{"id": "1"}, {"id": "99"}]
    result = await reconciler.reconcile(source, target)
    assert "99" in result["extra_in_target"]
