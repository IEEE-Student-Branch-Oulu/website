"""User + MembershipPeriod ORM models.

`status` and `role` are stored, not derived. `consents` is JSONB so we
can record consent versions and timestamps without a column-per-policy
explosion (privacy v1.0, terms v1.0, optional newsletter, optional
photo_release). Soft-delete uses `deleted_at` for GDPR right-to-erasure
while retaining audit log integrity.

Memberships are valid per academic year. `MembershipPeriod` tracks each
year's application/renewal status independently. `User.status` reflects
the *current* period's state so auth checks stay simple.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Role(StrEnum):
    member = "member"
    admin = "admin"


class UserStatus(StrEnum):
    pending_email = "pending_email"
    pending_approval = "pending_approval"
    active = "active"
    rejected = "rejected"
    suspended = "suspended"


class StudyLevel(StrEnum):
    bsc = "bsc"
    msc = "msc"
    phd = "phd"
    postdoc = "postdoc"
    other = "other"


class MembershipStatus(StrEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    lapsed = "lapsed"


class Visibility(StrEnum):
    public = "public"
    members = "members"
    private = "private"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Email is case-insensitive unique via the lower(email) index below.
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)

    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name="user_role", native_enum=True),
        nullable=False,
        default=Role.member,
    )
    status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus, name="user_status", native_enum=True),
        nullable=False,
        default=UserStatus.pending_email,
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    ieee_membership_number: Mapped[str] = mapped_column(String(20), nullable=False)
    ieee_grade: Mapped[str | None] = mapped_column(String(40))
    university: Mapped[str] = mapped_column(
        String(120), nullable=False, default="University of Oulu"
    )
    study_level: Mapped[StudyLevel | None] = mapped_column(
        SQLEnum(StudyLevel, name="study_level", native_enum=True)
    )
    study_program: Mapped[str | None] = mapped_column(String(120))
    expected_graduation_year: Mapped[int | None] = mapped_column(Integer)

    bio: Mapped[str | None] = mapped_column(Text)
    profile_visibility: Mapped[Visibility] = mapped_column(
        SQLEnum(Visibility, name="visibility", native_enum=True),
        nullable=False,
        default=Visibility.private,
    )

    # {"privacy":{"version":"1.0","accepted_at":"..."},
    #  "terms":   {"version":"1.0","accepted_at":"..."},
    #  "newsletter":     {"accepted_at":"..."} | null,
    #  "photo_release":  {"accepted_at":"..."} | null}
    consents: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("uq_users_email_lower", func.lower(email), unique=True),
        Index("ix_users_status", "status"),
        Index("ix_users_role_status", "role", "status"),
        Index(
            "ix_users_active",
            "deleted_at",
            postgresql_where="deleted_at IS NULL",
        ),
    )


class MembershipPeriod(Base):
    """One row per user per academic year.

    The academic year runs Sep-Aug. ``period_year`` stores the start year
    (e.g. 2026 for the 2026-2027 period).  The first row is created at
    registration; subsequent rows are created when the member clicks
    "Renew" — pre-filled, zero friction.  Admins approve/reject each
    period independently (typically at a board meeting).
    """

    __tablename__ = "membership_periods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    period_year: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    status: Mapped[MembershipStatus] = mapped_column(
        SQLEnum(MembershipStatus, name="membership_status", native_enum=True),
        nullable=False,
        default=MembershipStatus.pending,
    )

    ieee_membership_number: Mapped[str] = mapped_column(String(20), nullable=False)

    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    rejection_reason: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("uq_membership_user_year", "user_id", "period_year", unique=True),
        Index("ix_membership_status", "status"),
        Index("ix_membership_year_status", "period_year", "status"),
    )
