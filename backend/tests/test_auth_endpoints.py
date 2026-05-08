"""Integration tests for auth endpoints.

Exercises the full request path: routing → validation → service → DB → response.
Uses the ASGI client with a real database, so these verify HTTP status codes,
response shapes, and cookie behavior end-to-end.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.passwords import hash_password
from app.auth.sessions import COOKIE_NAME
from app.core.email import MemoryBackend, configure_backend, get_backend
from app.domains.members.models import User, UserStatus, Visibility
from tests.conftest import needs_db

_STRONG_PW = "correct-horse-battery-staple"
_CONSENTS = {"privacy": True, "terms": True}


@pytest.fixture(autouse=True)
def _use_memory_email() -> None:
    from app.config import get_settings

    get_settings().email_backend = "memory"
    configure_backend(MemoryBackend())


def _register_body(**overrides: object) -> dict:
    base = {
        "email": "test@example.com",
        "password": _STRONG_PW,
        "firstName": "Test",
        "lastName": "User",
        "ieeeMembershipNumber": "12345678",
        "consents": _CONSENTS,
    }
    base.update(overrides)
    return base


@needs_db
class TestRegisterEndpoint:
    async def test_register_returns_201(self, client: AsyncClient) -> None:
        resp = await client.post("/api/v1/auth/register", json=_register_body())
        assert resp.status_code == 201
        assert "email" in resp.json()["message"].lower()

    async def test_register_short_password_422(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/register",
            json=_register_body(password="short"),
        )
        assert resp.status_code == 422

    async def test_register_invalid_ieee_number_422(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/register",
            json=_register_body(ieeeMembershipNumber="ABC"),
        )
        assert resp.status_code == 422

    async def test_duplicate_email_still_returns_201(self, client: AsyncClient) -> None:
        await client.post("/api/v1/auth/register", json=_register_body())
        resp = await client.post("/api/v1/auth/register", json=_register_body())
        assert resp.status_code == 201


@needs_db
class TestLoginEndpoint:
    async def test_login_sets_session_cookie(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        db_session.add(
            User(
                email="alice@example.com",
                password_hash=hash_password(_STRONG_PW),
                first_name="Alice",
                last_name="Smith",
                ieee_membership_number="12345678",
                university="University of Oulu",
                profile_visibility=Visibility.private,
                consents=_CONSENTS,
                status=UserStatus.active,
            )
        )
        await db_session.commit()

        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "alice@example.com", "password": _STRONG_PW},
        )
        assert resp.status_code == 200
        assert COOKIE_NAME in resp.cookies
        body = resp.json()
        assert body["email"] == "alice@example.com"
        assert "membershipPeriods" in body

    async def test_login_wrong_password_401(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        db_session.add(
            User(
                email="alice@example.com",
                password_hash=hash_password(_STRONG_PW),
                first_name="Alice",
                last_name="Smith",
                ieee_membership_number="12345678",
                university="University of Oulu",
                profile_visibility=Visibility.private,
                consents=_CONSENTS,
                status=UserStatus.active,
            )
        )
        await db_session.commit()

        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "alice@example.com", "password": "wrong-password!!"},
        )
        assert resp.status_code == 401

    async def test_login_unknown_email_401(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@example.com", "password": _STRONG_PW},
        )
        assert resp.status_code == 401


@needs_db
class TestMeEndpoint:
    async def test_me_unauthenticated_401(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    async def test_me_authenticated_returns_profile(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        db_session.add(
            User(
                email="alice@example.com",
                password_hash=hash_password(_STRONG_PW),
                first_name="Alice",
                last_name="Smith",
                ieee_membership_number="12345678",
                university="University of Oulu",
                profile_visibility=Visibility.private,
                consents=_CONSENTS,
                status=UserStatus.active,
            )
        )
        await db_session.commit()

        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "alice@example.com", "password": _STRONG_PW},
        )
        token = login_resp.cookies[COOKIE_NAME]

        resp = await client.get("/api/v1/auth/me", cookies={COOKIE_NAME: token})
        assert resp.status_code == 200
        assert resp.json()["email"] == "alice@example.com"


@needs_db
class TestVerifyEmailEndpoint:
    async def test_invalid_token_returns_error(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/verify-email",
            json={"token": "bad-token"},
        )
        assert resp.status_code == 401


@needs_db
class TestForgotPasswordEndpoint:
    async def test_always_returns_204(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "nobody@example.com"},
        )
        assert resp.status_code == 204

    async def test_existing_user_sends_email(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        db_session.add(
            User(
                email="alice@example.com",
                password_hash=hash_password(_STRONG_PW),
                first_name="Alice",
                last_name="Smith",
                ieee_membership_number="12345678",
                university="University of Oulu",
                profile_visibility=Visibility.private,
                consents=_CONSENTS,
                status=UserStatus.active,
            )
        )
        await db_session.commit()

        resp = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "alice@example.com"},
        )
        assert resp.status_code == 204

        backend = get_backend()
        assert isinstance(backend, MemoryBackend)
        assert len(backend.outbox) == 1


@needs_db
class TestResendVerifyEndpoint:
    async def test_always_returns_204(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/resend-verify",
            json={"email": "nobody@example.com"},
        )
        assert resp.status_code == 204
