"""Data access for events. Only place that touches the SQLAlchemy session."""

from datetime import datetime

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.events.models import Event
from app.domains.events.schemas import EventStatus


def _status_filter_clause(status: EventStatus, now: datetime) -> tuple[ColumnElement[bool], ...]:
    """Translate a logical status filter into SQL clauses."""
    end_or_start = func.coalesce(Event.ends_at, Event.starts_at)
    if status == "upcoming":
        return (Event.starts_at > now,)
    if status == "past":
        return (end_or_start < now,)
    # ongoing
    return (Event.starts_at <= now, end_or_start >= now)


async def list_events(
    session: AsyncSession,
    *,
    limit: int,
    offset: int,
    status_filter: EventStatus | None,
    now: datetime,
) -> tuple[list[Event], int]:
    base = select(Event)
    count_q = select(func.count()).select_from(Event)
    if status_filter is not None:
        clauses = _status_filter_clause(status_filter, now)
        base = base.where(*clauses)
        count_q = count_q.where(*clauses)

    result = await session.execute(
        base.order_by(Event.starts_at.desc()).limit(limit).offset(offset)
    )
    items = list(result.scalars().all())
    total = (await session.execute(count_q)).scalar_one()
    return items, int(total)


async def get_next_upcoming(session: AsyncSession, *, now: datetime) -> Event | None:
    result = await session.execute(
        select(Event).where(Event.starts_at > now).order_by(Event.starts_at.asc()).limit(1)
    )
    return result.scalar_one_or_none()


async def get_by_slug(session: AsyncSession, *, slug: str) -> Event | None:
    result = await session.execute(select(Event).where(Event.slug == slug))
    return result.scalar_one_or_none()
