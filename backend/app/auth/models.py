"""Auth-owned ORM models: sessions, email tokens, audit log.

These tables support authentication and accountability concerns; they
reference `users.id` but are not part of the members domain.
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
    String,
    Text,
    func,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class EmailTokenKind(StrEnum):
    email_verify = "email_verify"
    password_reset = "password_reset"


class AuditAction(StrEnum):
    register = "register"
    login = "login"
    login_failed = "login_failed"
    logout = "logout"
    approve = "approve"
    reject = "reject"
    role_change = "role_change"
    suspend = "suspend"
    restore = "restore"
    profile_update = "profile_update"
    password_change = "password_change"
    membership_renew = "membership_renew"
    gdpr_export = "gdpr_export"
    gdpr_delete = "gdpr_delete"


class Session(Base):
    """Server-side session record. Cookie holds the raw token; we store its hash."""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    user_agent: Mapped[str | None] = mapped_column(String(255))
    ip: Mapped[str | None] = mapped_column(INET)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (Index("ix_sessions_user_revoked", "user_id", "revoked_at"),)


class EmailToken(Base):
    """Single-use token for email verification and password reset.

    The cleartext token is sent in the email; only its SHA-256 hash is stored.
    """

    __tablename__ = "email_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kind: Mapped[EmailTokenKind] = mapped_column(
        SQLEnum(EmailTokenKind, name="email_token_kind", native_enum=True),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (Index("ix_email_tokens_user_kind", "user_id", "kind"),)


class AuditLog(Base):
    """Append-only record of security-relevant actions.

    Foreign keys use SET NULL so soft-deleting a user preserves history
    while removing the strict identity link.
    """

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    action: Mapped[AuditAction] = mapped_column(
        SQLEnum(AuditAction, name="audit_action", native_enum=True), nullable=False
    )
    target_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    audit_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, nullable=False, default=dict
    )
    ip: Mapped[str | None] = mapped_column(INET)
    user_agent: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_audit_target_created", "target_user_id", "created_at"),
        Index("ix_audit_action_created", "action", "created_at"),
    )
