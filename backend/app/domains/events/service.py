"""Business logic for events.

Pure functions where possible — date math, status derivation, display
formatting — and a thin layer that orchestrates repository calls.
"""

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.errors import NotFoundError
from app.domains.events import repository
from app.domains.events.models import Event
from app.domains.events.schemas import (
    EventCreate,
    EventEdit,
    EventRead,
    EventStatus,
    EventUpdate,
)

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
        cover_image_url=event.cover_image_url,
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


async def get_for_edit(session: AsyncSession, event_id: int) -> EventEdit:
    event = await repository.get_by_id(session, event_id=event_id)
    if event is None:
        raise NotFoundError(f"Event {event_id} not found.")
    return EventEdit.model_validate(event, from_attributes=True)


def _to_utc(value: datetime) -> datetime:
    """Naive datetimes are interpreted in the branch timezone, then stored UTC."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=ZoneInfo(get_settings().timezone))
    return value.astimezone(UTC)


async def _unique_slug(session: AsyncSession, title: str, *, exclude_id: int | None = None) -> str:
    base = slugify(title) or "event"
    slug = base
    n = 2
    while await repository.slug_exists(session, slug=slug, exclude_id=exclude_id):
        slug = f"{base}-{n}"
        n += 1
    return slug


async def create_event(session: AsyncSession, data: EventCreate) -> EventRead:
    event = Event(
        title=data.title,
        slug=await _unique_slug(session, data.title),
        description=data.description,
        starts_at=_to_utc(data.starts_at),
        ends_at=_to_utc(data.ends_at) if data.ends_at else None,
        location=data.location,
        location_url=data.location_url,
        type=data.type,
        rsvp_link=data.rsvp_link,
        capacity=data.capacity,
        speaker_name=data.speaker_name,
        speaker_title=data.speaker_title,
        is_highlighted=data.is_highlighted,
        tags=data.tags,
        cover_image_url=data.cover_image_url,
    )
    event = await repository.add(session, event)
    await session.commit()
    return to_read(event)


async def update_event(session: AsyncSession, event_id: int, data: EventUpdate) -> EventRead:
    event = await repository.get_by_id(session, event_id=event_id)
    if event is None:
        raise NotFoundError(f"Event {event_id} not found.")

    fields = data.model_dump(exclude_unset=True)
    if "title" in fields:
        event.title = fields["title"]
        event.slug = await _unique_slug(session, fields["title"], exclude_id=event.id)
    if "starts_at" in fields and fields["starts_at"] is not None:
        event.starts_at = _to_utc(fields["starts_at"])
    if "ends_at" in fields:
        event.ends_at = _to_utc(fields["ends_at"]) if fields["ends_at"] else None
    for key in (
        "description",
        "location",
        "location_url",
        "type",
        "rsvp_link",
        "capacity",
        "speaker_name",
        "speaker_title",
        "is_highlighted",
        "tags",
        "cover_image_url",
    ):
        if key in fields:
            setattr(event, key, fields[key])

    await session.commit()
    await session.refresh(event)
    return to_read(event)


async def delete_event(session: AsyncSession, event_id: int) -> None:
    event = await repository.get_by_id(session, event_id=event_id)
    if event is None:
        raise NotFoundError(f"Event {event_id} not found.")
    await repository.delete(session, event)
    await session.commit()
