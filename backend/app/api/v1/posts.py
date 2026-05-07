"""HTTP routes for blog posts."""

from typing import Annotated

from fastapi import APIRouter, Query

from app.core.pagination import Page
from app.deps import DBSession, PaginationDep
from app.domains.posts import service
from app.domains.posts.schemas import PostCategory, PostFull, PostMeta

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
