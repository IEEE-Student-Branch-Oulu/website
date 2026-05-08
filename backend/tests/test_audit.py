"""Tests for the audit log recording helper."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import AuditAction, AuditLog
from app.core.audit import record
from tests.conftest import needs_db


@needs_db
class TestAuditRecord:
    async def test_creates_entry(self, db_session: AsyncSession) -> None:
        entry = await record(
            db_session,
            action=AuditAction.login,
            actor_user_id=1,
            target_user_id=1,
        )
        assert entry.action == AuditAction.login
        assert entry.actor_user_id == 1
        assert entry.audit_metadata == {}

    async def test_stores_metadata(self, db_session: AsyncSession) -> None:
        entry = await record(
            db_session,
            action=AuditAction.role_change,
            actor_user_id=1,
            target_user_id=2,
            metadata={"old_role": "member", "new_role": "admin"},
        )
        assert entry.audit_metadata["old_role"] == "member"

    async def test_without_request(self, db_session: AsyncSession) -> None:
        entry = await record(
            db_session,
            action=AuditAction.register,
            actor_user_id=1,
        )
        assert entry.ip is None
        assert entry.user_agent is None

    async def test_extracts_ip_and_ua_from_request(self, db_session: AsyncSession) -> None:
        from starlette.requests import Request

        scope = {
            "type": "http",
            "method": "POST",
            "path": "/test",
            "headers": [(b"user-agent", b"TestBrowser/1.0")],
            "server": ("localhost", 8000),
            "client": ("192.168.1.1", 12345),
        }
        request = Request(scope)
        entry = await record(
            db_session,
            action=AuditAction.login,
            actor_user_id=1,
            request=request,
        )
        assert entry.ip == "192.168.1.1"
        assert entry.user_agent == "TestBrowser/1.0"

    async def test_entry_persists(self, db_session: AsyncSession) -> None:
        await record(db_session, action=AuditAction.logout, actor_user_id=1)
        await db_session.flush()
        rows = (await db_session.execute(select(AuditLog))).scalars().all()
        assert len(rows) == 1
        assert rows[0].action == AuditAction.logout
