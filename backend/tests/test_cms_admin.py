"""DB-backed tests for CMS admin endpoints: authz + post/event CRUD.

Skipped unless a test database is configured (see conftest.needs_db).
"""

from __future__ import annotations

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.csrf import CSRF_COOKIE, CSRF_HEADER
from app.auth.passwords import hash_password
from app.auth.sessions import COOKIE_NAME, create_session
from app.domains.members.models import Role, User, UserStatus
from tests.conftest import needs_db

_CSRF = "test-csrf-token"


@pytest_asyncio.fixture(autouse=True)
async def _reset_global_engine() -> object:
    """``load_session`` updates last_seen via the global engine; its pooled
    connections bind to the first test's event loop. Dispose after each test
    so later tests (new loops) get fresh connections."""
    yield
    from app.db import engine

    await engine.dispose()


@pytest_asyncio.fixture
async def admin_cookies(db_session: AsyncSession) -> dict[str, str]:
    """Create an active admin + session; return cookies for authenticated calls."""
    admin = User(
        email="admin@example.com",
        password_hash=hash_password("password123"),
        first_name="Ada",
        last_name="Admin",
        role=Role.admin,
        status=UserStatus.active,
        ieee_membership_number="12345678",
    )
    db_session.add(admin)
    await db_session.flush()
    raw, _ = await create_session(db_session, user_id=admin.id)
    await db_session.commit()
    return {COOKIE_NAME: raw, CSRF_COOKIE: _CSRF}


def _post_body(**overrides: object) -> dict:
    body = {
        "title": "GNU Radio Recap",
        "excerpt": "What we built.",
        "bodyMd": "## Intro\n\nWe built a radar.",
        "category": "event-recap",
        "tags": ["sdr"],
        "eventSlug": "gnu-radio-workshop",
    }
    body.update(overrides)
    return body


def _event_body(**overrides: object) -> dict:
    body = {
        "title": "AI Workshop",
        "description": "Hands-on session.",
        "startsAt": "2026-09-01T13:00:00+03:00",
        "endsAt": "2026-09-01T17:00:00+03:00",
        "location": "TS101",
        "type": "workshop",
        "capacity": 30,
        "tags": ["ai"],
    }
    body.update(overrides)
    return body


@needs_db
class TestAuthz:
    async def test_create_post_requires_auth(self, client: AsyncClient) -> None:
        resp = await client.post("/api/v1/posts", json=_post_body())
        assert resp.status_code == 401

    async def test_create_event_requires_auth(self, client: AsyncClient) -> None:
        resp = await client.post("/api/v1/events", json=_event_body())
        assert resp.status_code == 401

    async def test_delete_post_requires_auth(self, client: AsyncClient) -> None:
        resp = await client.delete("/api/v1/posts/1")
        assert resp.status_code == 401


@needs_db
class TestPostCrud:
    async def test_create_then_fetch_and_delete(
        self, client: AsyncClient, admin_cookies: dict[str, str]
    ) -> None:
        headers = {CSRF_HEADER: _CSRF}
        created = await client.post(
            "/api/v1/posts", json=_post_body(), cookies=admin_cookies, headers=headers
        )
        assert created.status_code == 201
        data = created.json()
        assert data["slug"] == "gnu-radio-recap"
        assert data["eventSlug"] == "gnu-radio-workshop"
        assert data["author"] == "Ada Admin"
        assert "bodyHtml" in data
        post_id = data["id"]

        # Public read by slug works without auth.
        public = await client.get(f"/api/v1/posts/{data['slug']}")
        assert public.status_code == 200

        # Raw edit fetch returns markdown source.
        raw = await client.get(f"/api/v1/posts/{post_id}/raw", cookies=admin_cookies)
        assert raw.status_code == 200
        assert raw.json()["bodyMd"].startswith("## Intro")

        deleted = await client.delete(
            f"/api/v1/posts/{post_id}", cookies=admin_cookies, headers=headers
        )
        assert deleted.status_code == 204

    async def test_duplicate_title_gets_unique_slug(
        self, client: AsyncClient, admin_cookies: dict[str, str]
    ) -> None:
        headers = {CSRF_HEADER: _CSRF}
        first = await client.post(
            "/api/v1/posts", json=_post_body(), cookies=admin_cookies, headers=headers
        )
        second = await client.post(
            "/api/v1/posts", json=_post_body(), cookies=admin_cookies, headers=headers
        )
        assert first.json()["slug"] == "gnu-radio-recap"
        assert second.json()["slug"] == "gnu-radio-recap-2"


@needs_db
class TestEventCrud:
    async def test_create_update_delete(
        self, client: AsyncClient, admin_cookies: dict[str, str]
    ) -> None:
        headers = {CSRF_HEADER: _CSRF}
        created = await client.post(
            "/api/v1/events", json=_event_body(), cookies=admin_cookies, headers=headers
        )
        assert created.status_code == 201
        event_id = created.json()["id"]
        assert created.json()["slug"] == "ai-workshop"

        updated = await client.put(
            f"/api/v1/events/{event_id}",
            json={"location": "TS135"},
            cookies=admin_cookies,
            headers=headers,
        )
        assert updated.status_code == 200
        assert updated.json()["location"] == "TS135"

        deleted = await client.delete(
            f"/api/v1/events/{event_id}", cookies=admin_cookies, headers=headers
        )
        assert deleted.status_code == 204


@needs_db
class TestAuditTrail:
    async def test_post_lifecycle_is_audited(
        self, client: AsyncClient, admin_cookies: dict[str, str]
    ) -> None:
        headers = {CSRF_HEADER: _CSRF}
        created = await client.post(
            "/api/v1/posts", json=_post_body(), cookies=admin_cookies, headers=headers
        )
        post_id = created.json()["id"]
        await client.put(
            f"/api/v1/posts/{post_id}",
            json={"title": "GNU Radio Recap v2"},
            cookies=admin_cookies,
            headers=headers,
        )
        await client.delete(f"/api/v1/posts/{post_id}", cookies=admin_cookies, headers=headers)

        audit = await client.get("/api/v1/admin/audit", cookies=admin_cookies)
        actions = [e["action"] for e in audit.json()["items"]]
        assert "content_create" in actions
        assert "content_update" in actions
        assert "content_delete" in actions

        create_entry = next(e for e in audit.json()["items"] if e["action"] == "content_create")
        assert create_entry["metadata"]["kind"] == "post"
        assert create_entry["metadata"]["title"] == "GNU Radio Recap"
