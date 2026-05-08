"""Pydantic schemas for User responses and profile updates."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.domains.members.models import (
    MembershipStatus,
    Role,
    StudyLevel,
    UserStatus,
    Visibility,
)


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class MembershipPeriodRead(_CamelModel):
    id: int
    period_year: int
    status: MembershipStatus
    ieee_membership_number: str
    applied_at: datetime
    reviewed_at: datetime | None = None


class UserPublic(_CamelModel):
    """Public directory card — opt-in via profile_visibility=public."""

    id: int
    first_name: str
    last_name: str
    university: str
    study_level: StudyLevel | None = None
    study_program: str | None = None
    bio: str | None = None


class UserSelf(_CamelModel):
    """Full profile returned to the authenticated user."""

    id: int
    email: str
    first_name: str
    last_name: str
    role: Role
    status: UserStatus
    email_verified_at: datetime | None = None
    ieee_membership_number: str
    ieee_grade: str | None = None
    university: str
    study_level: StudyLevel | None = None
    study_program: str | None = None
    expected_graduation_year: int | None = None
    bio: str | None = None
    profile_visibility: Visibility
    consents: dict[str, Any]
    created_at: datetime
    membership_periods: list[MembershipPeriodRead] = Field(default_factory=list)


class UserAdmin(_CamelModel):
    """Admin view — includes status, role, timestamps."""

    id: int
    email: str
    first_name: str
    last_name: str
    role: Role
    status: UserStatus
    email_verified_at: datetime | None = None
    ieee_membership_number: str
    ieee_grade: str | None = None
    university: str
    study_level: StudyLevel | None = None
    study_program: str | None = None
    expected_graduation_year: int | None = None
    profile_visibility: Visibility
    consents: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    membership_periods: list[MembershipPeriodRead] = Field(default_factory=list)


class ProfileUpdate(_CamelModel):
    """Fields a member can edit on their own profile."""

    first_name: str | None = None
    last_name: str | None = None
    ieee_grade: str | None = None
    university: str | None = None
    study_level: StudyLevel | None = None
    study_program: str | None = None
    expected_graduation_year: int | None = Field(default=None, ge=1900, le=2100)
    bio: str | None = None
    profile_visibility: Visibility | None = None
