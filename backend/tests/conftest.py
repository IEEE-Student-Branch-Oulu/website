"""Shared pytest fixtures.

Pure-logic tests (most of `app/domains/*/service.py`, `app/core/*`) need no
database — they run anywhere. Integration tests that hit `app.main` and the
DB are skipped unless `TEST_DATABASE_URL` (or a reachable
`postgresql+asyncpg://...` `DATABASE_URL`) is configured. CI sets one; local
contributors get full coverage by running `make test` after `make dev` is up.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base


def _resolve_test_db_url() -> str | None:
    return os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")


_TEST_DB_URL = _resolve_test_db_url()
needs_db = pytest.mark.skipif(
    _TEST_DB_URL is None,
    reason="Set TEST_DATABASE_URL (or DATABASE_URL) to run DB-backed tests.",
)


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    assert _TEST_DB_URL is not None  # guarded by needs_db
    engine = create_async_engine(_TEST_DB_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    """ASGI test client with the DB dependency overridden to share `db_session`."""
    from app.db import get_db
    from app.main import create_app

    app = create_app()

    async def _override_get_db() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
