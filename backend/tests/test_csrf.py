"""Tests for the double-submit CSRF middleware.

Verifies:
- Safe methods (GET, HEAD, OPTIONS) are always allowed.
- Mutating requests from authenticated sessions require a matching CSRF token.
- Unauthenticated requests bypass CSRF checks.
- A CSRF cookie is set on responses that don't already have one.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from app.auth.csrf import CSRF_COOKIE, CSRF_HEADER, CSRFMiddleware
from app.auth.sessions import COOKIE_NAME as SESSION_COOKIE


async def _ok(request: Request) -> JSONResponse:
    return JSONResponse({"ok": True})


def _make_app() -> Starlette:
    app = Starlette(
        routes=[
            Route("/test", _ok, methods=["GET", "POST", "DELETE"]),
        ],
    )
    app.add_middleware(CSRFMiddleware)
    return app


@pytest.fixture
def app() -> Starlette:
    return _make_app()


@pytest.fixture
async def client(app: Starlette) -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


class TestSafeMethods:
    async def test_get_always_passes(self, client: AsyncClient) -> None:
        resp = await client.get("/test")
        assert resp.status_code == 200

    async def test_get_sets_csrf_cookie_when_absent(self, client: AsyncClient) -> None:
        resp = await client.get("/test")
        assert CSRF_COOKIE in resp.cookies


class TestUnauthenticated:
    async def test_post_without_session_is_allowed(self, client: AsyncClient) -> None:
        resp = await client.post("/test")
        assert resp.status_code == 200


class TestAuthenticated:
    async def test_post_without_csrf_header_is_rejected(self, client: AsyncClient) -> None:
        resp = await client.post("/test", cookies={SESSION_COOKIE: "fake-session"})
        assert resp.status_code == 403

    async def test_post_with_mismatched_token_is_rejected(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/test",
            cookies={SESSION_COOKIE: "fake-session", CSRF_COOKIE: "token-a"},
            headers={CSRF_HEADER: "token-b"},
        )
        assert resp.status_code == 403

    async def test_post_with_matching_token_passes(self, client: AsyncClient) -> None:
        token = "valid-csrf-token"
        resp = await client.post(
            "/test",
            cookies={SESSION_COOKIE: "fake-session", CSRF_COOKIE: token},
            headers={CSRF_HEADER: token},
        )
        assert resp.status_code == 200

    async def test_delete_enforces_csrf(self, client: AsyncClient) -> None:
        resp = await client.delete("/test", cookies={SESSION_COOKIE: "fake-session"})
        assert resp.status_code == 403


class TestCookieLifecycle:
    async def test_existing_csrf_cookie_is_not_overwritten(self, client: AsyncClient) -> None:
        resp = await client.get("/test", cookies={CSRF_COOKIE: "existing"})
        assert CSRF_COOKIE not in resp.cookies
