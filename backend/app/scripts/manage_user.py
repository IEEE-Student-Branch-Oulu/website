"""CLI to manage users: promote to admin, activate membership.

Usage:
  uv run python -m app.scripts.manage_user promote user@example.com
  uv run python -m app.scripts.manage_user activate user@example.com
"""

from __future__ import annotations

import asyncio
import sys

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionLocal
from app.domains.members.models import MembershipPeriod, MembershipStatus, Role, User, UserStatus


async def promote(email: str) -> None:
    async with SessionLocal() as db:
        user = await _get_user(db, email)

        if user.role == Role.admin:
            print(f"{email} is already an admin.")
            return

        await db.execute(update(User).where(User.id == user.id).values(role=Role.admin))
        await db.commit()
        print(f"Promoted {email} to admin.")


async def activate(email: str) -> None:
    async with SessionLocal() as db:
        user = await _get_user(db, email)

        if user.status == UserStatus.active:
            print(f"{email} is already active.")
            return

        await db.execute(update(User).where(User.id == user.id).values(status=UserStatus.active))

        await db.execute(
            update(MembershipPeriod)
            .where(
                MembershipPeriod.user_id == user.id,
                MembershipPeriod.status == MembershipStatus.pending,
            )
            .values(status=MembershipStatus.approved)
        )

        await db.commit()
        print(f"Activated {email} (status → active, pending periods → approved).")


async def _get_user(db: AsyncSession, email: str) -> User:
    stmt = select(User).where(func.lower(User.email) == email.lower())
    user = (await db.execute(stmt)).scalar_one_or_none()
    if user is None:
        print(f"No user found with email: {email}")
        sys.exit(1)
    return user


COMMANDS = {
    "promote": promote,
    "activate": activate,
}


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in COMMANDS:
        print("Usage: uv run python -m app.scripts.manage_user <command> <email>")
        print(f"Commands: {', '.join(COMMANDS)}")
        sys.exit(1)

    command = COMMANDS[sys.argv[1]]
    asyncio.run(command(sys.argv[2]))


if __name__ == "__main__":
    main()
