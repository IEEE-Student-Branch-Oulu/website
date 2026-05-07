"""Business logic for events.

Pure functions where possible — date math, status derivation, display
formatting — and a thin layer that orchestrates repository calls.
"""

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.errors import NotFoundError
from app.domains.events import repository
from app.domains.events.models import Event
from app.domains.events.schemas import EventRead, EventStatus

_WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_RANGE_DASH = "–"  # noqa: RUF001 -- en-dash, matches frontend timeDisplay style


def _now_utc() -> datetime:
    return datetime.now(tz=UTC)


def derive_status(starts_at: datetime, ends_at: datetime | None, now: datetime) -> EventStatus:
    """Return the event's status relative to ``now``."""
    end = ends_at or starts_at
    if now < starts_at:
        return "upcoming"
    if now > end:
        return "past"
    return "ongoing"


def derive_spots_left(capacity: int | None, attendees: int) -> int | None:
    if capacity is None:
        return None
    return max(0, capacity - attendees)


def format_display(starts_at: datetime, ends_at: datetime | None, tz_name: str) -> tuple[str, str]:
    """Render dateDisplay + timeDisplay in the branch timezone."""
    tz = ZoneInfo(tz_name)
    start_local = starts_at.astimezone(tz)
    date_display = (
        f"{_WEEKDAY[start_local.weekday()]}, "
        f"{_MONTH[start_local.month - 1]} {start_local.day}, {start_local.year}"
    )

    tz_abbr = start_local.tzname() or tz_name
    if ends_at is None:
        time_display = f"{start_local:%H:%M} {tz_abbr}"
    else:
        end_local = ends_at.astimezone(tz)
        if end_local.date() == start_local.date():
            time_display = f"{start_local:%H:%M} {_RANGE_DASH} {end_local:%H:%M} {tz_abbr}"
        else:
            time_display = (
                f"{start_local:%H:%M} {_RANGE_DASH} "
                f"{_MONTH[end_local.month - 1]} {end_local.day}, {end_local:%H:%M} {tz_abbr}"
            )
    return date_display, time_display


def to_read(event: Event, *, now: datetime | None = None) -> EventRead:
    now = now or _now_utc()
    settings = get_settings()
    date_display, time_display = format_display(event.starts_at, event.ends_at, settings.timezone)
    return EventRead(
        id=event.id,
        title=event.title,
        slug=event.slug,
        description=event.description,
        date_iso=event.starts_at.isoformat(),
        date_display=date_display,
        time_display=time_display,
        location=event.location,
        location_url=event.location_url,
        type=event.type,
        status=derive_status(event.starts_at, event.ends_at, now),
        rsvp_link=event.rsvp_link,
        capacity=event.capacity,
        spots_left=derive_spots_left(event.capacity, event.attendees_count),
        tags=list(event.tags or []),
        speaker_name=event.speaker_name,
        speaker_title=event.speaker_title,
        is_highlighted=event.is_highlighted,
    )


async def list_events(
    session: AsyncSession,
    *,
    limit: int,
    offset: int,
    status_filter: EventStatus | None = None,
) -> tuple[list[EventRead], int]:
    now = _now_utc()
    rows, total = await repository.list_events(
        session, limit=limit, offset=offset, status_filter=status_filter, now=now
    )
    return [to_read(e, now=now) for e in rows], total


async def get_next_upcoming(session: AsyncSession) -> EventRead:
    now = _now_utc()
    event = await repository.get_next_upcoming(session, now=now)
    if event is None:
        raise NotFoundError("No upcoming events.")
    return to_read(event, now=now)


async def get_by_slug(session: AsyncSession, slug: str) -> EventRead:
    event = await repository.get_by_slug(session, slug=slug)
    if event is None:
        raise NotFoundError(f"Event '{slug}' not found.")
    return to_read(event)
