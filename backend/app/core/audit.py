"""Audit log helper — single function to record security-relevant actions."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.auth.models import AuditAction, AuditLog


async def record(
    db: AsyncSession,
    *,
    action: AuditAction,
    actor_user_id: int | None = None,
    target_user_id: int | None = None,
    metadata: dict[str, Any] | None = None,
    request: Request | None = None,
) -> AuditLog:
    ip: str | None = None
    user_agent: str | None = None
    if request is not None:
        ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

    entry = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        target_user_id=target_user_id,
        audit_metadata=metadata or {},
        ip=ip,
        user_agent=user_agent,
    )
    db.add(entry)
    return entry
