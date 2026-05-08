"""auth + members tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


user_role = postgresql.ENUM("member", "admin", name="user_role", create_type=False)
user_status = postgresql.ENUM(
    "pending_email",
    "pending_approval",
    "active",
    "rejected",
    "suspended",
    name="user_status",
    create_type=False,
)
study_level = postgresql.ENUM(
    "bsc", "msc", "phd", "postdoc", "other", name="study_level", create_type=False
)
visibility = postgresql.ENUM("public", "members", "private", name="visibility", create_type=False)
email_token_kind = postgresql.ENUM(
    "email_verify", "password_reset", name="email_token_kind", create_type=False
)
membership_status = postgresql.ENUM(
    "pending", "approved", "rejected", "lapsed",
    name="membership_status",
    create_type=False,
)
audit_action = postgresql.ENUM(
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
    name="audit_action",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    user_status.create(bind, checkfirst=True)
    study_level.create(bind, checkfirst=True)
    visibility.create(bind, checkfirst=True)
    email_token_kind.create(bind, checkfirst=True)
    membership_status.create(bind, checkfirst=True)
    audit_action.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default=sa.text("'member'::user_role"),
        ),
        sa.Column(
            "status",
            user_status,
            nullable=False,
            server_default=sa.text("'pending_email'::user_status"),
        ),
        sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ieee_membership_number", sa.String(length=20), nullable=False),
        sa.Column("ieee_grade", sa.String(length=40), nullable=True),
        sa.Column(
            "university",
            sa.String(length=120),
            nullable=False,
            server_default=sa.text("'University of Oulu'"),
        ),
        sa.Column("study_level", study_level, nullable=True),
        sa.Column("study_program", sa.String(length=120), nullable=True),
        sa.Column("expected_graduation_year", sa.Integer(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column(
            "profile_visibility",
            visibility,
            nullable=False,
            server_default=sa.text("'private'::visibility"),
        ),
        sa.Column(
            "consents",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "uq_users_email_lower", "users", [sa.text("lower(email)")], unique=True
    )
    op.create_index("ix_users_status", "users", ["status"])
    op.create_index("ix_users_role_status", "users", ["role", "status"])
    op.create_index(
        "ix_users_active",
        "users",
        ["deleted_at"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("ip", postgresql.INET(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("token_hash", name="uq_sessions_token_hash"),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_index("ix_sessions_user_revoked", "sessions", ["user_id", "revoked_at"])

    op.create_table(
        "email_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", email_token_kind, nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("token_hash", name="uq_email_tokens_token_hash"),
    )
    op.create_index("ix_email_tokens_user_id", "email_tokens", ["user_id"])
    op.create_index("ix_email_tokens_user_kind", "email_tokens", ["user_id", "kind"])

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "actor_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action", audit_action, nullable=False),
        sa.Column(
            "target_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("ip", postgresql.INET(), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_audit_target_created", "audit_log", ["target_user_id", "created_at"])
    op.create_index("ix_audit_action_created", "audit_log", ["action", "created_at"])

    op.create_table(
        "membership_periods",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("period_year", sa.SmallInteger(), nullable=False),
        sa.Column(
            "status",
            membership_status,
            nullable=False,
            server_default=sa.text("'pending'::membership_status"),
        ),
        sa.Column("ieee_membership_number", sa.String(length=20), nullable=False),
        sa.Column(
            "applied_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "reviewed_by",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.UniqueConstraint("user_id", "period_year", name="uq_membership_user_year"),
    )
    op.create_index("ix_membership_status", "membership_periods", ["status"])
    op.create_index(
        "ix_membership_year_status", "membership_periods", ["period_year", "status"]
    )


def downgrade() -> None:
    op.drop_index("ix_membership_year_status", table_name="membership_periods")
    op.drop_index("ix_membership_status", table_name="membership_periods")
    op.drop_table("membership_periods")

    op.drop_index("ix_audit_action_created", table_name="audit_log")
    op.drop_index("ix_audit_target_created", table_name="audit_log")
    op.drop_table("audit_log")

    op.drop_index("ix_email_tokens_user_kind", table_name="email_tokens")
    op.drop_index("ix_email_tokens_user_id", table_name="email_tokens")
    op.drop_table("email_tokens")

    op.drop_index("ix_sessions_user_revoked", table_name="sessions")
    op.drop_index("ix_sessions_user_id", table_name="sessions")
    op.drop_table("sessions")

    op.drop_index("ix_users_active", table_name="users")
    op.drop_index("ix_users_role_status", table_name="users")
    op.drop_index("ix_users_status", table_name="users")
    op.drop_index("uq_users_email_lower", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    audit_action.drop(bind, checkfirst=True)
    membership_status.drop(bind, checkfirst=True)
    email_token_kind.drop(bind, checkfirst=True)
    visibility.drop(bind, checkfirst=True)
    study_level.drop(bind, checkfirst=True)
    user_status.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
