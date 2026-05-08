"""Server-side session helpers: create, load, revoke, cookie config."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Session
from app.auth.tokens import generate_token, hash_token

COOKIE_NAME = "ieee_sid"
SESSION_IDLE_DAYS = 14
SESSION_ABSOLUTE_DAYS = 30


def set_session_cookie(response: object, token: str, *, secure: bool = True) -> None:
    """Set the session cookie on a Starlette/FastAPI Response."""
    from starlette.responses import Response as StarletteResponse

    assert isinstance(response, StarletteResponse)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
        max_age=60 * 60 * 24 * SESSION_IDLE_DAYS,
    )


def delete_session_cookie(response: object, *, secure: bool = True) -> None:
    """Clear the session cookie."""
    from starlette.responses import Response as StarletteResponse

    assert isinstance(response, StarletteResponse)
    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )


async def create_session(
    db: AsyncSession,
    *,
    user_id: int,
    user_agent: str | None = None,
    ip: str | None = None,
) -> tuple[str, Session]:
    """Create a new session row and return ``(raw_token, session)``."""
    raw, token_hash = generate_token()
    now = datetime.now(tz=UTC)
    session = Session(
        user_id=user_id,
        token_hash=token_hash,
        user_agent=_truncate(user_agent, 255),
        ip=ip,
        expires_at=now + timedelta(days=SESSION_ABSOLUTE_DAYS),
    )
    db.add(session)
    return raw, session


async def load_session(db: AsyncSession, raw_token: str) -> Session | None:
    """Look up a valid (not expired, not revoked) session by raw token."""
    h = hash_token(raw_token)
    now = datetime.now(tz=UTC)
    stmt = select(Session).where(
        Session.token_hash == h,
        Session.revoked_at.is_(None),
        Session.expires_at > now,
    )
    session = (await db.execute(stmt)).scalar_one_or_none()
    if session is None:
        return None

    idle_cutoff = now - timedelta(days=SESSION_IDLE_DAYS)
    if session.last_seen_at < idle_cutoff:
        return None

    session.last_seen_at = now
    return session


async def revoke_session(db: AsyncSession, session_id: int) -> None:
    await db.execute(
        update(Session)
        .where(Session.id == session_id, Session.revoked_at.is_(None))
        .values(revoked_at=datetime.now(tz=UTC))
    )


async def revoke_all_sessions(
    db: AsyncSession, user_id: int, *, except_session_id: int | None = None
) -> None:
    stmt = (
        update(Session)
        .where(Session.user_id == user_id, Session.revoked_at.is_(None))
        .values(revoked_at=datetime.now(tz=UTC))
    )
    if except_session_id is not None:
        stmt = stmt.where(Session.id != except_session_id)
    await db.execute(stmt)


def _truncate(value: str | None, max_len: int) -> str | None:
    if value is None:
        return None
    return value[:max_len]
