"""End-to-end smoke tests against the ASGI app.

Skipped automatically unless TEST_DATABASE_URL (or DATABASE_URL) points to a
reachable Postgres. CI configures this; locally `make dev` brings the DB up.
"""

from __future__ import annotations

from datetime import UTC, datetime

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.events.models import Event
from tests.conftest import needs_db


@needs_db
async def test_health(client: AsyncClient) -> None:
    res = await client.get("/api/v1/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@needs_db
async def test_events_list_empty(client: AsyncClient) -> None:
    res = await client.get("/api/v1/events")
    assert res.status_code == 200
    body = res.json()
    assert body == {"items": [], "total": 0, "limit": 20, "offset": 0}


@needs_db
async def test_event_by_slug_returns_camel_case(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    db_session.add(
        Event(
            title="Test Workshop",
            slug="test-workshop",
            description="d",
            starts_at=datetime(2099, 1, 1, 12, tzinfo=UTC),
            ends_at=datetime(2099, 1, 1, 14, tzinfo=UTC),
            location="L",
            type="workshop",
            tags=["a", "b"],
            capacity=10,
            attendees_count=2,
        )
    )
    await db_session.commit()

    res = await client.get("/api/v1/events/test-workshop")
    assert res.status_code == 200
    body = res.json()
    assert body["dateISO"].startswith("2099-")
    assert "dateDisplay" in body and "timeDisplay" in body
    assert body["spotsLeft"] == 8
    assert body["status"] == "upcoming"


@needs_db
async def test_event_by_slug_404_problem_json(client: AsyncClient) -> None:
    res = await client.get("/api/v1/events/does-not-exist")
    assert res.status_code == 404
    assert res.headers["content-type"].startswith("application/problem+json")
    body = res.json()
    assert body["status"] == 404
    assert body["title"] == "Not Found"


@needs_db
async def test_validation_error_returns_problem_json(client: AsyncClient) -> None:
    res = await client.get("/api/v1/events?limit=9999")
    assert res.status_code == 422
    assert res.headers["content-type"].startswith("application/problem+json")
