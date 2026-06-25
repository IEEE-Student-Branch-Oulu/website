"""HTTP routes for blog posts."""

from typing import Annotated

from fastapi import APIRouter, Query, Request, status

from app.auth.dependencies import RequireAdmin
from app.auth.models import AuditAction
from app.core.audit import record
from app.core.pagination import Page
from app.deps import DBSession, PaginationDep
from app.domains.posts import service
from app.domains.posts.schemas import (
    PostCategory,
    PostCreate,
    PostEdit,
    PostFull,
    PostMeta,
    PostUpdate,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", summary="List blog posts", response_model=Page[PostMeta])
async def list_posts(
    db: DBSession,
    page: PaginationDep,
    category: Annotated[PostCategory | None, Query(description="Filter by category")] = None,
) -> Page[PostMeta]:
    items, total = await service.list_posts(
        db, limit=page.limit, offset=page.offset, category=category
    )
    return Page[PostMeta](items=items, total=total, limit=page.limit, offset=page.offset)


@router.get("/{slug}", summary="Post by slug", response_model=PostFull)
async def post_by_slug(slug: str, db: DBSession) -> PostFull:
    return await service.get_by_slug(db, slug)


@router.post(
    "",
    summary="Create a post",
    response_model=PostFull,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    body: PostCreate, request: Request, db: DBSession, admin: RequireAdmin
) -> PostFull:
    post = await service.create_post(
        db,
        body,
        default_author_name=f"{admin.first_name} {admin.last_name}".strip(),
        default_author_role="IEEE SB Oulu",
    )
    await record(
        db,
        action=AuditAction.content_create,
        actor_user_id=admin.id,
        metadata={"kind": "post", "id": post.id, "slug": post.slug, "title": post.title},
        request=request,
    )
    await db.commit()
    return post


@router.get("/{post_id}/raw", summary="Raw post for editing", response_model=PostEdit)
async def post_raw(post_id: int, db: DBSession, _admin: RequireAdmin) -> PostEdit:
    return await service.get_for_edit(db, post_id)


@router.put("/{post_id}", summary="Update a post", response_model=PostFull)
async def update_post(
    post_id: int, body: PostUpdate, request: Request, db: DBSession, admin: RequireAdmin
) -> PostFull:
    post = await service.update_post(db, post_id, body)
    await record(
        db,
        action=AuditAction.content_update,
        actor_user_id=admin.id,
        metadata={"kind": "post", "id": post.id, "slug": post.slug, "title": post.title},
        request=request,
    )
    await db.commit()
    return post


@router.delete("/{post_id}", summary="Delete a post", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, request: Request, db: DBSession, admin: RequireAdmin) -> None:
    await service.delete_post(db, post_id)
    await record(
        db,
        action=AuditAction.content_delete,
        actor_user_id=admin.id,
        metadata={"kind": "post", "id": post_id},
        request=request,
    )
    await db.commit()
