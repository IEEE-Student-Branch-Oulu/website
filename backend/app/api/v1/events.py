"""HTTP routes for events."""

from typing import Annotated

from fastapi import APIRouter, Query

from app.core.pagination import Page
from app.deps import DBSession, PaginationDep
from app.domains.events import service
from app.domains.events.schemas import EventRead, EventStatus

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", summary="List events", response_model=Page[EventRead])
async def list_events(
    db: DBSession,
    page: PaginationDep,
    status: Annotated[EventStatus | None, Query(description="Filter by status")] = None,
) -> Page[EventRead]:
    items, total = await service.list_events(
        db, limit=page.limit, offset=page.offset, status_filter=status
    )
    return Page[EventRead](items=items, total=total, limit=page.limit, offset=page.offset)


@router.get("/next", summary="Next upcoming event", response_model=EventRead)
async def next_event(db: DBSession) -> EventRead:
    return await service.get_next_upcoming(db)


@router.get("/{slug}", summary="Event by slug", response_model=EventRead)
async def event_by_slug(slug: str, db: DBSession) -> EventRead:
    return await service.get_by_slug(db, slug)
