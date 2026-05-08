"""Tests for the member repository — data access layer.

Tests the query logic: filtering, pagination, soft-delete exclusion,
directory visibility, and membership period queries.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.members.models import (
    MembershipPeriod,
    MembershipStatus,
    Role,
    User,
    UserStatus,
    Visibility,
)
from app.domains.members.repository import (
    count_active_admins,
    email_exists,
    get_by_email,
    get_by_id,
    list_directory,
    list_paged,
    list_pending_approval,
    list_pending_renewals,
    list_periods,
)
from tests.conftest import needs_db


def _make_user(email: str = "test@example.com", **overrides: object) -> User:
    defaults = dict(
        email=email,
        password_hash="$argon2id$fake",
        first_name="Test",
        last_name="User",
        ieee_membership_number="12345678",
        university="University of Oulu",
        profile_visibility=Visibility.private,
        consents={"privacy": True, "terms": True},
        status=UserStatus.active,
    )
    defaults.update(overrides)
    return User(**defaults)


@needs_db
class TestGetById:
    async def test_existing_user(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()
        result = await get_by_id(db_session, user.id)
        assert result is not None
        assert result.email == "test@example.com"

    async def test_nonexistent_returns_none(self, db_session: AsyncSession) -> None:
        result = await get_by_id(db_session, 99999)
        assert result is None

    async def test_soft_deleted_excluded_by_default(self, db_session: AsyncSession) -> None:
        user = _make_user()
        user.deleted_at = datetime.now(tz=UTC)
        db_session.add(user)
        await db_session.flush()
        assert await get_by_id(db_session, user.id) is None

    async def test_soft_deleted_included_with_flag(self, db_session: AsyncSession) -> None:
        user = _make_user()
        user.deleted_at = datetime.now(tz=UTC)
        db_session.add(user)
        await db_session.flush()
        result = await get_by_id(db_session, user.id, include_deleted=True)
        assert result is not None


@needs_db
class TestGetByEmail:
    async def test_case_insensitive(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user(email="Alice@Example.COM"))
        await db_session.flush()
        result = await get_by_email(db_session, "alice@example.com")
        assert result is not None

    async def test_nonexistent(self, db_session: AsyncSession) -> None:
        result = await get_by_email(db_session, "nobody@example.com")
        assert result is None


@needs_db
class TestEmailExists:
    async def test_existing(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user())
        await db_session.flush()
        assert await email_exists(db_session, "test@example.com") is True

    async def test_not_existing(self, db_session: AsyncSession) -> None:
        assert await email_exists(db_session, "nope@example.com") is False


@needs_db
class TestListPaged:
    async def test_empty_returns_zero(self, db_session: AsyncSession) -> None:
        rows, total = await list_paged(db_session, limit=10, offset=0)
        assert rows == []
        assert total == 0

    async def test_pagination(self, db_session: AsyncSession) -> None:
        for i in range(5):
            db_session.add(_make_user(email=f"user{i}@example.com"))
        await db_session.flush()

        rows, total = await list_paged(db_session, limit=2, offset=0)
        assert len(rows) == 2
        assert total == 5

    async def test_filter_by_status(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user(email="active@e.com", status=UserStatus.active))
        db_session.add(_make_user(email="pending@e.com", status=UserStatus.pending_approval))
        await db_session.flush()

        rows, total = await list_paged(
            db_session, limit=10, offset=0, status=UserStatus.pending_approval
        )
        assert total == 1
        assert rows[0].email == "pending@e.com"

    async def test_filter_by_role(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user(email="admin@e.com", role=Role.admin))
        db_session.add(_make_user(email="member@e.com", role=Role.member))
        await db_session.flush()

        rows, total = await list_paged(db_session, limit=10, offset=0, role=Role.admin)
        assert total == 1
        assert rows[0].role == Role.admin

    async def test_search_by_name(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user(email="a@e.com", first_name="Alice", last_name="Smith"))
        db_session.add(_make_user(email="b@e.com", first_name="Bob", last_name="Jones"))
        await db_session.flush()

        rows, total = await list_paged(db_session, limit=10, offset=0, q="alice")
        assert total == 1
        assert rows[0].first_name == "Alice"

    async def test_search_by_email(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user(email="findme@special.com"))
        db_session.add(_make_user(email="other@example.com"))
        await db_session.flush()

        _, total = await list_paged(db_session, limit=10, offset=0, q="findme")
        assert total == 1

    async def test_excludes_soft_deleted(self, db_session: AsyncSession) -> None:
        user = _make_user()
        user.deleted_at = datetime.now(tz=UTC)
        db_session.add(user)
        await db_session.flush()

        _, total = await list_paged(db_session, limit=10, offset=0)
        assert total == 0


@needs_db
class TestListPendingApproval:
    async def test_only_pending_users(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user(email="pending@e.com", status=UserStatus.pending_approval))
        db_session.add(_make_user(email="active@e.com", status=UserStatus.active))
        await db_session.flush()

        rows, total = await list_pending_approval(db_session, limit=10, offset=0)
        assert total == 1
        assert rows[0].status == UserStatus.pending_approval


@needs_db
class TestListDirectory:
    async def test_only_public_active_members(self, db_session: AsyncSession) -> None:
        db_session.add(
            _make_user(
                email="pub@e.com",
                profile_visibility=Visibility.public,
                status=UserStatus.active,
            )
        )
        db_session.add(
            _make_user(
                email="priv@e.com",
                profile_visibility=Visibility.private,
                status=UserStatus.active,
            )
        )
        db_session.add(
            _make_user(
                email="pending@e.com",
                profile_visibility=Visibility.public,
                status=UserStatus.pending_approval,
            )
        )
        await db_session.flush()

        rows, total = await list_directory(db_session, limit=10, offset=0)
        assert total == 1
        assert rows[0].email == "pub@e.com"


@needs_db
class TestCountActiveAdmins:
    async def test_counts_only_active_admins(self, db_session: AsyncSession) -> None:
        db_session.add(_make_user(email="admin1@e.com", role=Role.admin, status=UserStatus.active))
        db_session.add(
            _make_user(email="admin2@e.com", role=Role.admin, status=UserStatus.suspended)
        )
        db_session.add(_make_user(email="member@e.com", role=Role.member, status=UserStatus.active))
        await db_session.flush()

        count = await count_active_admins(db_session)
        assert count == 1


@needs_db
class TestMembershipPeriods:
    async def test_list_periods_ordered_by_year_desc(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        for year in (2023, 2025, 2024):
            db_session.add(
                MembershipPeriod(
                    user_id=user.id,
                    period_year=year,
                    ieee_membership_number="12345678",
                    status=MembershipStatus.approved,
                )
            )
        await db_session.flush()

        periods = await list_periods(db_session, user.id)
        assert [p.period_year for p in periods] == [2025, 2024, 2023]

    async def test_list_pending_renewals(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        db_session.add(
            MembershipPeriod(
                user_id=user.id,
                period_year=2025,
                ieee_membership_number="12345678",
                status=MembershipStatus.pending,
            )
        )
        db_session.add(
            MembershipPeriod(
                user_id=user.id,
                period_year=2024,
                ieee_membership_number="12345678",
                status=MembershipStatus.approved,
            )
        )
        await db_session.flush()

        rows, total = await list_pending_renewals(db_session, year=2025, limit=10, offset=0)
        assert total == 1
        assert rows[0].period_year == 2025
