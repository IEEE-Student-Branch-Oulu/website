"""Tests for the member service layer — profile updates, GDPR, soft delete."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.members.models import (
    MembershipPeriod,
    MembershipStatus,
    StudyLevel,
    User,
    UserStatus,
    Visibility,
)
from app.domains.members.schemas import ProfileUpdate
from app.domains.members.service import (
    gdpr_export,
    get_self_with_periods,
    soft_delete,
    update_profile,
)
from tests.conftest import needs_db


def _make_user(**overrides: object) -> User:
    defaults = dict(
        email="test@example.com",
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
class TestUpdateProfile:
    async def test_partial_update(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        updates = ProfileUpdate(bio="Hi!", university="Aalto")
        result = await update_profile(db_session, user, updates)
        assert result.bio == "Hi!"
        assert result.university == "Aalto"
        assert result.first_name == "Test"

    async def test_empty_update_changes_nothing(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        updates = ProfileUpdate()
        result = await update_profile(db_session, user, updates)
        assert result.first_name == "Test"

    async def test_update_visibility(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        updates = ProfileUpdate(profile_visibility=Visibility.public)
        result = await update_profile(db_session, user, updates)
        assert result.profile_visibility == Visibility.public

    async def test_update_study_fields(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        updates = ProfileUpdate(
            study_level=StudyLevel.msc,
            study_program="Computer Science",
            expected_graduation_year=2027,
        )
        result = await update_profile(db_session, user, updates)
        assert result.study_level == StudyLevel.msc
        assert result.study_program == "Computer Science"
        assert result.expected_graduation_year == 2027


@needs_db
class TestGetSelfWithPeriods:
    async def test_includes_periods(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        period = MembershipPeriod(
            user_id=user.id,
            period_year=2025,
            ieee_membership_number="12345678",
            status=MembershipStatus.approved,
        )
        db_session.add(period)
        await db_session.flush()

        result = await get_self_with_periods(db_session, user)
        assert len(result.membership_periods) == 1
        assert result.membership_periods[0].period_year == 2025

    async def test_no_periods(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        result = await get_self_with_periods(db_session, user)
        assert result.membership_periods == []


@needs_db
class TestGdprExport:
    async def test_export_structure(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        data = await gdpr_export(db_session, user)
        assert "user" in data
        assert "membership_periods" in data
        assert "exported_at" in data
        assert data["user"]["email"] == "test@example.com"

    async def test_export_includes_periods(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        period = MembershipPeriod(
            user_id=user.id,
            period_year=2025,
            ieee_membership_number="12345678",
            status=MembershipStatus.pending,
        )
        db_session.add(period)
        await db_session.flush()

        data = await gdpr_export(db_session, user)
        assert len(data["membership_periods"]) == 1


@needs_db
class TestSoftDelete:
    async def test_anonymizes_user(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        await soft_delete(db_session, user)
        assert user.deleted_at is not None
        assert "deleted" in user.email
        assert user.first_name == "Deleted"
        assert user.last_name == "User"
        assert user.bio is None
        assert user.consents == {}

    async def test_deleted_at_is_set(self, db_session: AsyncSession) -> None:
        user = _make_user()
        db_session.add(user)
        await db_session.flush()

        before = datetime.now(tz=UTC)
        await soft_delete(db_session, user)
        assert user.deleted_at >= before
