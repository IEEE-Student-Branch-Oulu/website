"""Argon2id password hashing + HIBP k-anonymity breach check."""

from __future__ import annotations

import hashlib
import logging

import httpx
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

log = logging.getLogger(__name__)

_ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)

DUMMY_HASH = _ph.hash("not-a-real-password")


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(password: str, hash_: str) -> bool:
    try:
        return _ph.verify(hash_, password)
    except VerifyMismatchError:
        return False


def needs_rehash(hash_: str) -> bool:
    return _ph.check_needs_rehash(hash_)


def verify_dummy(password: str) -> None:
    """Constant-time comparison against a dummy hash to prevent timing leaks."""
    verify_password(password, DUMMY_HASH)


async def is_password_breached(password: str) -> bool:
    """Check HIBP Pwned Passwords via k-anonymity (range API).

    Returns True if the password appears in a known breach.
    Fails open on network errors — we don't block registration if HIBP is down.
    """
    sha1 = hashlib.sha1(password.encode(), usedforsecurity=False).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                timeout=3.0,
            )
            resp.raise_for_status()
    except httpx.HTTPError:
        log.warning("HIBP API unreachable — failing open")
        return False

    for line in resp.text.splitlines():
        hash_suffix, _, count = line.partition(":")
        if hash_suffix.strip() == suffix and int(count.strip()) > 0:
            return True
    return False
