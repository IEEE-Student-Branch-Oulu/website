"""Business logic for posts: rendering, mapping, lookups."""

import math
from datetime import UTC, date, datetime

from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.markdown import render
from app.domains.posts import repository
from app.domains.posts.models import Post
from app.domains.posts.schemas import (
    PostCreate,
    PostEdit,
    PostFull,
    PostMeta,
    PostUpdate,
    TocHeading,
)

_WORDS_PER_MINUTE = 200

_MONTH_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _format_date(d: date) -> str:
    return f"{_MONTH_SHORT[d.month - 1]} {d.day}, {d.year}"


def _read_time(minutes: int) -> str:
    return f"{minutes} min read"


def to_meta(post: Post) -> PostMeta:
    return PostMeta(
        id=post.id,
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        category=post.category,
        author=post.author_name,
        author_initials=post.author_initials,
        author_role=post.author_role,
        date=_format_date(post.published_on),
        date_iso=post.published_on.isoformat(),
        read_time=_read_time(post.read_minutes),
        tags=list(post.tags or []),
        featured=post.featured,
        cover_image_url=post.cover_image_url,
        event_slug=post.event_slug,
    )


def to_full(post: Post) -> PostFull:
    rendered = render(post.body_md)
    meta = to_meta(post)
    return PostFull(
        **meta.model_dump(by_alias=False),
        headings=[TocHeading(id=h.id, text=h.text, level=h.level) for h in rendered.headings],
        body_html=rendered.html,
    )


async def list_posts(
    session: AsyncSession, *, limit: int, offset: int, category: str | None = None
) -> tuple[list[PostMeta], int]:
    rows, total = await repository.list_posts(
        session, limit=limit, offset=offset, category=category
    )
    return [to_meta(p) for p in rows], total


async def get_by_slug(session: AsyncSession, slug: str) -> PostFull:
    post = await repository.get_by_slug(session, slug=slug)
    if post is None:
        raise NotFoundError(f"Post '{slug}' not found.")
    return to_full(post)


async def get_for_edit(session: AsyncSession, post_id: int) -> PostEdit:
    post = await repository.get_by_id(session, post_id=post_id)
    if post is None:
        raise NotFoundError(f"Post {post_id} not found.")
    return PostEdit.model_validate(post, from_attributes=True)


def _read_minutes(body_md: str) -> int:
    return max(1, math.ceil(len(body_md.split()) / _WORDS_PER_MINUTE))


def _initials(name: str) -> str:
    parts = [p for p in name.split() if p]
    return "".join(p[0].upper() for p in parts[:2]) or "?"


async def _unique_slug(session: AsyncSession, title: str, *, exclude_id: int | None = None) -> str:
    base = slugify(title) or "post"
    slug = base
    n = 2
    while await repository.slug_exists(session, slug=slug, exclude_id=exclude_id):
        slug = f"{base}-{n}"
        n += 1
    return slug


async def create_post(
    session: AsyncSession,
    data: PostCreate,
    *,
    default_author_name: str,
    default_author_role: str,
) -> PostFull:
    author_name = data.author_name or default_author_name
    post = Post(
        title=data.title,
        slug=await _unique_slug(session, data.title),
        excerpt=data.excerpt,
        body_md=data.body_md,
        category=data.category,
        author_name=author_name,
        author_initials=data.author_initials or _initials(author_name),
        author_role=data.author_role or default_author_role,
        published_on=data.published_on or datetime.now(tz=UTC).date(),
        read_minutes=_read_minutes(data.body_md),
        tags=data.tags,
        featured=data.featured,
        cover_image_url=data.cover_image_url,
        event_slug=data.event_slug,
    )
    post = await repository.add(session, post)
    await session.commit()
    return to_full(post)


async def update_post(session: AsyncSession, post_id: int, data: PostUpdate) -> PostFull:
    post = await repository.get_by_id(session, post_id=post_id)
    if post is None:
        raise NotFoundError(f"Post {post_id} not found.")

    fields = data.model_dump(exclude_unset=True)
    if "title" in fields:
        post.title = fields["title"]
        post.slug = await _unique_slug(session, fields["title"], exclude_id=post.id)
    for key in (
        "excerpt",
        "body_md",
        "category",
        "tags",
        "featured",
        "cover_image_url",
        "event_slug",
        "published_on",
        "author_name",
        "author_initials",
        "author_role",
    ):
        if key in fields:
            setattr(post, key, fields[key])
    if "body_md" in fields:
        post.read_minutes = _read_minutes(post.body_md)

    await session.commit()
    await session.refresh(post)
    return to_full(post)


async def delete_post(session: AsyncSession, post_id: int) -> None:
    post = await repository.get_by_id(session, post_id=post_id)
    if post is None:
        raise NotFoundError(f"Post {post_id} not found.")
    await repository.delete(session, post)
    await session.commit()
