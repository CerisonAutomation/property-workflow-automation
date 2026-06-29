"""Tests for HMAC webhook signature verification."""
import hmac
import hashlib
from security.webhook_verification import verify_guesty_signature


def _make_sig(body: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def test_valid_signature_passes():
    body = b'{"event":"reservation.created"}'
    secret = "test-secret"
    sig = _make_sig(body, secret)
    assert verify_guesty_signature(body, sig, secret) is True


def test_invalid_signature_fails():
    body = b'{"event":"reservation.created"}'
    assert verify_guesty_signature(body, "wrong-sig", "test-secret") is False


def test_empty_signature_fails():
    body = b'{"event":"reservation.created"}'
    assert verify_guesty_signature(body, "", "test-secret") is False
