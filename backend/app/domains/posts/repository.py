"""Data access for posts."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.posts.models import Post


async def list_posts(
    session: AsyncSession, *, limit: int, offset: int, category: str | None
) -> tuple[list[Post], int]:
    base = select(Post)
    count_q = select(func.count()).select_from(Post)
    if category is not None:
        base = base.where(Post.category == category)
        count_q = count_q.where(Post.category == category)

    result = await session.execute(
        base.order_by(Post.published_on.desc(), Post.id.desc()).limit(limit).offset(offset)
    )
    items = list(result.scalars().all())
    total = (await session.execute(count_q)).scalar_one()
    return items, int(total)


async def get_by_slug(session: AsyncSession, *, slug: str) -> Post | None:
    result = await session.execute(select(Post).where(Post.slug == slug))
    return result.scalar_one_or_none()


async def get_by_id(session: AsyncSession, *, post_id: int) -> Post | None:
    return await session.get(Post, post_id)


async def slug_exists(session: AsyncSession, *, slug: str, exclude_id: int | None = None) -> bool:
    q = select(Post.id).where(Post.slug == slug)
    if exclude_id is not None:
        q = q.where(Post.id != exclude_id)
    return (await session.execute(q)).first() is not None


async def add(session: AsyncSession, post: Post) -> Post:
    session.add(post)
    await session.flush()
    await session.refresh(post)
    return post


async def delete(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
