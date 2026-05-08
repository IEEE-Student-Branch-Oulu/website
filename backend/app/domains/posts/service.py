"""Business logic for posts: rendering, mapping, lookups."""

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.markdown import render
from app.domains.posts import repository
from app.domains.posts.models import Post
from app.domains.posts.schemas import PostFull, PostMeta, TocHeading

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
