"""HTTP routes for events."""

from typing import Annotated

from fastapi import APIRouter, Query, Request, status

from app.auth.dependencies import RequireAdmin
from app.auth.models import AuditAction
from app.core.audit import record
from app.core.pagination import Page
from app.deps import DBSession, PaginationDep
from app.domains.events import service
from app.domains.events.schemas import (
    EventCreate,
    EventEdit,
    EventRead,
    EventStatus,
    EventUpdate,
)

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


@router.post(
    "",
    summary="Create an event",
    response_model=EventRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    body: EventCreate, request: Request, db: DBSession, admin: RequireAdmin
) -> EventRead:
    event = await service.create_event(db, body)
    await record(
        db,
        action=AuditAction.content_create,
        actor_user_id=admin.id,
        metadata={"kind": "event", "id": event.id, "slug": event.slug, "title": event.title},
        request=request,
    )
    await db.commit()
    return event


@router.get("/{event_id}/raw", summary="Raw event for editing", response_model=EventEdit)
async def event_raw(event_id: int, db: DBSession, _admin: RequireAdmin) -> EventEdit:
    return await service.get_for_edit(db, event_id)


@router.put("/{event_id}", summary="Update an event", response_model=EventRead)
async def update_event(
    event_id: int, body: EventUpdate, request: Request, db: DBSession, admin: RequireAdmin
) -> EventRead:
    event = await service.update_event(db, event_id, body)
    await record(
        db,
        action=AuditAction.content_update,
        actor_user_id=admin.id,
        metadata={"kind": "event", "id": event.id, "slug": event.slug, "title": event.title},
        request=request,
    )
    await db.commit()
    return event


@router.delete("/{event_id}", summary="Delete an event", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, request: Request, db: DBSession, admin: RequireAdmin) -> None:
    await service.delete_event(db, event_id)
    await record(
        db,
        action=AuditAction.content_delete,
        actor_user_id=admin.id,
        metadata={"kind": "event", "id": event_id},
        request=request,
    )
    await db.commit()
