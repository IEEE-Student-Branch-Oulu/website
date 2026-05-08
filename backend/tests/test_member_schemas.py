"""Tests for member Pydantic schemas — serialization and validation."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.domains.members.models import (
    MembershipStatus,
    Role,
    StudyLevel,
    UserStatus,
    Visibility,
)
from app.domains.members.schemas import (
    MembershipPeriodRead,
    ProfileUpdate,
    UserAdmin,
    UserPublic,
    UserSelf,
)


def _user_self_data(**overrides: object) -> dict:
    base = {
        "id": 1,
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Smith",
        "role": Role.member,
        "status": UserStatus.active,
        "ieee_membership_number": "12345678",
        "university": "University of Oulu",
        "profile_visibility": Visibility.private,
        "consents": {"privacy": True, "terms": True},
        "created_at": datetime(2025, 1, 1, tzinfo=UTC),
    }
    base.update(overrides)
    return base


class TestUserSelf:
    def test_required_fields(self) -> None:
        user = UserSelf(**_user_self_data())
        assert user.email == "alice@example.com"
        assert user.membership_periods == []

    def test_optional_fields_default_none(self) -> None:
        user = UserSelf(**_user_self_data())
        assert user.email_verified_at is None
        assert user.bio is None
        assert user.study_level is None

    def test_camel_case_serialization(self) -> None:
        user = UserSelf(**_user_self_data())
        d = user.model_dump(by_alias=True)
        assert "firstName" in d
        assert "ieeeMembershipNumber" in d
        assert "profileVisibility" in d

    def test_with_membership_periods(self) -> None:
        period = MembershipPeriodRead(
            id=1,
            period_year=2025,
            status=MembershipStatus.approved,
            ieee_membership_number="12345678",
            applied_at=datetime(2025, 9, 1, tzinfo=UTC),
        )
        user = UserSelf(**_user_self_data(), membership_periods=[period])
        assert len(user.membership_periods) == 1
        assert user.membership_periods[0].period_year == 2025


class TestUserPublic:
    def test_excludes_sensitive_fields(self) -> None:
        pub = UserPublic(
            id=1,
            first_name="Alice",
            last_name="Smith",
            university="University of Oulu",
        )
        d = pub.model_dump()
        assert "email" not in d
        assert "password_hash" not in d
        assert "consents" not in d


class TestUserAdmin:
    def test_includes_timestamps(self) -> None:
        now = datetime(2025, 6, 1, tzinfo=UTC)
        admin = UserAdmin(
            **_user_self_data(),
            updated_at=now,
        )
        assert admin.updated_at == now
        assert admin.deleted_at is None


class TestProfileUpdate:
    def test_all_optional(self) -> None:
        update = ProfileUpdate()
        assert update.model_dump(exclude_unset=True) == {}

    def test_partial_update(self) -> None:
        update = ProfileUpdate(bio="Hi there", university="Aalto")
        dumped = update.model_dump(exclude_unset=True)
        assert dumped == {"bio": "Hi there", "university": "Aalto"}
        assert "first_name" not in dumped

    def test_graduation_year_validation(self) -> None:
        ProfileUpdate(expected_graduation_year=2028)
        with pytest.raises(ValidationError):
            ProfileUpdate(expected_graduation_year=1899)

    def test_study_level_enum(self) -> None:
        update = ProfileUpdate(study_level=StudyLevel.msc)
        assert update.study_level == StudyLevel.msc

    def test_visibility_enum(self) -> None:
        update = ProfileUpdate(profile_visibility=Visibility.public)
        assert update.profile_visibility == Visibility.public


class TestMembershipPeriodRead:
    def test_camel_case_output(self) -> None:
        period = MembershipPeriodRead(
            id=1,
            period_year=2025,
            status=MembershipStatus.pending,
            ieee_membership_number="12345678",
            applied_at=datetime(2025, 9, 1, tzinfo=UTC),
        )
        d = period.model_dump(by_alias=True)
        assert "periodYear" in d
        assert "ieeeMembershipNumber" in d
        assert "appliedAt" in d
