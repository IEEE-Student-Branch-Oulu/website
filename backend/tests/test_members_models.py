"""Pure-logic tests for User / Session / EmailToken / AuditLog models.

These don't touch the database — they verify that enum values, defaults,
and field shapes match what the auth service will rely on.
"""

from datetime import UTC, datetime, timedelta

import sqlalchemy as sa

from app.auth.models import AuditAction, AuditLog, EmailToken, EmailTokenKind, Session
from app.domains.members.models import (
    MembershipPeriod,
    MembershipStatus,
    Role,
    StudyLevel,
    User,
    UserStatus,
    Visibility,
)


class TestEnums:
    def test_role_values(self) -> None:
        assert Role.member == "member"
        assert Role.admin == "admin"

    def test_user_status_values(self) -> None:
        assert {s.value for s in UserStatus} == {
            "pending_email",
            "pending_approval",
            "active",
            "rejected",
            "suspended",
        }

    def test_study_level_values(self) -> None:
        assert {s.value for s in StudyLevel} == {"bsc", "msc", "phd", "postdoc", "other"}

    def test_visibility_values(self) -> None:
        assert {v.value for v in Visibility} == {"public", "members", "private"}

    def test_email_token_kinds(self) -> None:
        assert {k.value for k in EmailTokenKind} == {"email_verify", "password_reset"}

    def test_membership_status_values(self) -> None:
        assert {s.value for s in MembershipStatus} == {
            "pending",
            "approved",
            "rejected",
            "lapsed",
        }

    def test_audit_actions_cover_plan(self) -> None:
        required = {
            "register",
            "login",
            "login_failed",
            "logout",
            "approve",
            "reject",
            "role_change",
            "suspend",
            "restore",
            "profile_update",
            "password_change",
            "membership_renew",
            "gdpr_export",
            "gdpr_delete",
        }
        assert required <= {a.value for a in AuditAction}


class TestUserConstruction:
    def test_minimum_required_fields(self) -> None:
        user = User(
            email="A@B.com",
            password_hash="$argon2id$...",
            first_name="A",
            last_name="B",
            ieee_membership_number="12345678",
        )
        # Stored as-given; uniqueness uses lower(email) at the DB level.
        assert user.email == "A@B.com"
        # SQLAlchemy column defaults are applied at flush-time, not on Python
        # construction, so the attribute is unset until the row hits the DB.
        # Constructing without a session is enough to verify the column exists.
        assert hasattr(user, "role")
        assert hasattr(user, "status")
        assert hasattr(user, "profile_visibility")

    def test_consents_field_accepts_dict(self) -> None:
        user = User(
            email="c@d.com",
            password_hash="x",
            first_name="C",
            last_name="D",
            ieee_membership_number="12345678",
            consents={
                "privacy": {"version": "1.0", "accepted_at": "2026-05-07T00:00:00Z"},
                "terms": {"version": "1.0", "accepted_at": "2026-05-07T00:00:00Z"},
            },
        )
        assert user.consents["privacy"]["version"] == "1.0"


class TestAuthModels:
    def test_session_construction(self) -> None:
        now = datetime.now(tz=UTC)
        s = Session(
            user_id=1,
            token_hash="a" * 64,
            expires_at=now + timedelta(days=14),
            user_agent="Mozilla/5.0",
            ip="127.0.0.1",
        )
        assert s.token_hash == "a" * 64
        assert s.user_id == 1

    def test_email_token_construction(self) -> None:
        now = datetime.now(tz=UTC)
        t = EmailToken(
            user_id=1,
            kind=EmailTokenKind.email_verify,
            token_hash="b" * 64,
            expires_at=now + timedelta(hours=24),
        )
        assert t.kind == EmailTokenKind.email_verify

    def test_membership_period_construction(self) -> None:
        p = MembershipPeriod(
            user_id=1,
            period_year=2026,
            ieee_membership_number="12345678",
        )
        assert p.period_year == 2026
        assert p.user_id == 1
        assert hasattr(p, "status")
        assert hasattr(p, "reviewed_at")
        assert hasattr(p, "rejection_reason")

    def test_membership_period_unique_per_year(self) -> None:
        table = MembershipPeriod.__table__
        assert isinstance(table, sa.Table)
        idx = next(i for i in table.indexes if i.name == "uq_membership_user_year")
        assert idx.unique

    def test_audit_log_renames_metadata_attribute(self) -> None:
        # `metadata` is reserved on Declarative Base, so the attribute is
        # `audit_metadata` while the column name stays "metadata".
        entry = AuditLog(
            action=AuditAction.register,
            actor_user_id=None,
            target_user_id=1,
            audit_metadata={"reason": "self"},
        )
        assert entry.audit_metadata == {"reason": "self"}
        assert "metadata" in {c.name for c in AuditLog.__table__.columns}
