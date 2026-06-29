"""Secure webhook verification utilities.
Supports HMAC-SHA256, JWT, and token-based verification.
"""

import hmac
import hashlib
import time
import jwt
from typing import Optional


def verify_hmac_webhook(payload: bytes, signature: str, secret: str) -> bool:
    """Verify a webhook payload using HMAC-SHA256."""
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


def verify_jwt_token(token: str, secret: str, algorithm: str = "HS256") -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        return jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.PyJWTError:
        return None


def is_request_fresh(timestamp: str, max_age_seconds: int = 300) -> bool:
    """Prevent replay attacks by checking request freshness."""
    try:
        request_time = int(timestamp)
        return abs(time.time() - request_time) <= max_age_seconds
    except (ValueError, TypeError):
        return False
