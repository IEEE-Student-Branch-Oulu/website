"""Member service — profile updates, GDPR, directory."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.members.models import User
from app.domains.members.repository import list_periods
from app.domains.members.schemas import MembershipPeriodRead, ProfileUpdate, UserSelf


def to_user_self(user: User, periods: list[MembershipPeriodRead] | None = None) -> UserSelf:
    data = UserSelf.model_validate(user, from_attributes=True)
    if periods is not None:
        data.membership_periods = periods
    return data


async def get_self_with_periods(db: AsyncSession, user: User) -> UserSelf:
    periods = await list_periods(db, user.id)
    period_reads = [MembershipPeriodRead.model_validate(p, from_attributes=True) for p in periods]
    return to_user_self(user, period_reads)


async def update_profile(db: AsyncSession, user: User, updates: ProfileUpdate) -> User:
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    return user


async def gdpr_export(db: AsyncSession, user: User) -> dict[str, Any]:
    periods = await list_periods(db, user.id)
    return {
        "user": UserSelf.model_validate(user, from_attributes=True).model_dump(mode="json"),
        "membership_periods": [
            MembershipPeriodRead.model_validate(p, from_attributes=True).model_dump(mode="json")
            for p in periods
        ],
        "exported_at": datetime.now(tz=UTC).isoformat(),
    }


async def soft_delete(db: AsyncSession, user: User) -> None:
    user.deleted_at = datetime.now(tz=UTC)
    user.email = f"deleted-{user.id}@deleted.invalid"
    user.first_name = "Deleted"
    user.last_name = "User"
    user.bio = None
    user.consents = {}
