"""Single-use token generation (email verification, password reset).

The raw token is sent to the user; only its SHA-256 hash is stored.
"""

from __future__ import annotations

import hashlib
import secrets


def generate_token() -> tuple[str, str]:
    """Return ``(raw_token, token_hash)``.

    ``raw_token`` is 32 bytes of URL-safe base64.
    ``token_hash`` is the lowercase hex SHA-256 of the raw token.
    """
    raw = secrets.token_urlsafe(32)
    h = hashlib.sha256(raw.encode()).hexdigest()
    return raw, h


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()
