"""Tests for reservation-driven access control."""
import pytest
from workflows.access_control import AccessController


@pytest.fixture
def controller():
    return AccessController(gate_callback_url="http://localhost:9999/gate")


def test_generate_code_is_deterministic(controller):
    code1 = controller._generate_code("res-123", "2026-08-01")
    code2 = controller._generate_code("res-123", "2026-08-01")
    assert code1 == code2


def test_generate_code_is_6_digits(controller):
    code = controller._generate_code("res-abc", "2026-09-01")
    assert len(code) == 6
    assert code.isdigit()


def test_different_reservations_get_different_codes(controller):
    code1 = controller._generate_code("res-001", "2026-08-01")
    code2 = controller._generate_code("res-002", "2026-08-01")
    assert code1 != code2
