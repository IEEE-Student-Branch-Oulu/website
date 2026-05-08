"""Data access for users.

Service-layer code calls these helpers — routers never touch the session
directly. Soft-deleted rows (`deleted_at IS NOT NULL`) are excluded from
the default queries; admin-facing queries that need them must opt in via
`include_deleted=True`.
"""

from __future__ import annotations

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.members.models import (
    MembershipPeriod,
    MembershipStatus,
    Role,
    User,
    UserStatus,
    Visibility,
)


def _active_only(stmt: Select[tuple[User]]) -> Select[tuple[User]]:
    return stmt.where(User.deleted_at.is_(None))


async def get_by_id(
    session: AsyncSession, user_id: int, *, include_deleted: bool = False
) -> User | None:
    stmt = select(User).where(User.id == user_id)
    if not include_deleted:
        stmt = _active_only(stmt)
    return (await session.execute(stmt)).scalar_one_or_none()


async def get_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = _active_only(select(User).where(func.lower(User.email) == email.lower()))
    return (await session.execute(stmt)).scalar_one_or_none()


async def email_exists(session: AsyncSession, email: str) -> bool:
    return (await get_by_email(session, email)) is not None


async def list_paged(
    session: AsyncSession,
    *,
    limit: int,
    offset: int,
    status: UserStatus | None = None,
    role: Role | None = None,
    q: str | None = None,
    include_deleted: bool = False,
) -> tuple[list[User], int]:
    stmt = select(User)
    count_stmt = select(func.count()).select_from(User)
    if not include_deleted:
        stmt = _active_only(stmt)
        count_stmt = count_stmt.where(User.deleted_at.is_(None))
    if status is not None:
        stmt = stmt.where(User.status == status)
        count_stmt = count_stmt.where(User.status == status)
    if role is not None:
        stmt = stmt.where(User.role == role)
        count_stmt = count_stmt.where(User.role == role)
    if q:
        like = f"%{q.lower()}%"
        clause = func.lower(User.email).like(like) | func.lower(
            User.first_name + " " + User.last_name
        ).like(like)
        stmt = stmt.where(clause)
        count_stmt = count_stmt.where(clause)

    rows = (
        (await session.execute(stmt.order_by(User.created_at.desc()).limit(limit).offset(offset)))
        .scalars()
        .all()
    )
    total = (await session.execute(count_stmt)).scalar_one()
    return list(rows), int(total)


async def list_pending_approval(
    session: AsyncSession, *, limit: int, offset: int
) -> tuple[list[User], int]:
    return await list_paged(session, limit=limit, offset=offset, status=UserStatus.pending_approval)


async def list_directory(
    session: AsyncSession, *, limit: int, offset: int
) -> tuple[list[User], int]:
    """Active members who opted into the public directory."""
    stmt = _active_only(
        select(User).where(
            User.status == UserStatus.active,
            User.profile_visibility == Visibility.public,
        )
    )
    count_stmt = (
        select(func.count())
        .select_from(User)
        .where(
            User.deleted_at.is_(None),
            User.status == UserStatus.active,
            User.profile_visibility == Visibility.public,
        )
    )
    rows = (
        (
            await session.execute(
                stmt.order_by(User.last_name.asc(), User.first_name.asc())
                .limit(limit)
                .offset(offset)
            )
        )
        .scalars()
        .all()
    )
    total = (await session.execute(count_stmt)).scalar_one()
    return list(rows), int(total)


async def count_active_admins(session: AsyncSession) -> int:
    """Used by the last-admin guard."""
    stmt = (
        select(func.count())
        .select_from(User)
        .where(
            User.deleted_at.is_(None),
            User.role == Role.admin,
            User.status == UserStatus.active,
        )
    )
    return int((await session.execute(stmt)).scalar_one())


def add(session: AsyncSession, user: User) -> User:
    session.add(user)
    return user


# ── Membership periods ──────────────────────────────────────────────


async def get_period(session: AsyncSession, user_id: int, year: int) -> MembershipPeriod | None:
    stmt = select(MembershipPeriod).where(
        MembershipPeriod.user_id == user_id,
        MembershipPeriod.period_year == year,
    )
    return (await session.execute(stmt)).scalar_one_or_none()


async def get_current_period(session: AsyncSession, user_id: int) -> MembershipPeriod | None:
    stmt = (
        select(MembershipPeriod)
        .where(MembershipPeriod.user_id == user_id)
        .order_by(MembershipPeriod.period_year.desc())
        .limit(1)
    )
    return (await session.execute(stmt)).scalar_one_or_none()


async def list_periods(session: AsyncSession, user_id: int) -> list[MembershipPeriod]:
    stmt = (
        select(MembershipPeriod)
        .where(MembershipPeriod.user_id == user_id)
        .order_by(MembershipPeriod.period_year.desc())
    )
    return list((await session.execute(stmt)).scalars().all())


async def list_pending_renewals(
    session: AsyncSession, *, year: int, limit: int, offset: int
) -> tuple[list[MembershipPeriod], int]:
    base = select(MembershipPeriod).where(
        MembershipPeriod.period_year == year,
        MembershipPeriod.status == MembershipStatus.pending,
    )
    count_stmt = (
        select(func.count())
        .select_from(MembershipPeriod)
        .where(
            MembershipPeriod.period_year == year,
            MembershipPeriod.status == MembershipStatus.pending,
        )
    )
    stmt = base.order_by(MembershipPeriod.applied_at.asc()).limit(limit).offset(offset)
    rows = (await session.execute(stmt)).scalars().all()
    total = (await session.execute(count_stmt)).scalar_one()
    return list(rows), int(total)


def add_period(session: AsyncSession, period: MembershipPeriod) -> MembershipPeriod:
    session.add(period)
    return period
