"""Auth service — orchestrates registration, login, email verification, password flows."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import EmailToken, EmailTokenKind
from app.auth.passwords import (
    hash_password,
    is_password_breached,
    needs_rehash,
    verify_dummy,
    verify_password,
)
from app.auth.tokens import generate_token, hash_token
from app.config import get_settings
from app.core.email import EmailMessage, get_backend, render
from app.core.errors import AuthenticationError, ConflictError, DomainError
from app.domains.members.models import (
    MembershipPeriod,
    MembershipStatus,
    User,
    UserStatus,
    Visibility,
)
from app.domains.members.repository import get_by_email


class WeakPasswordError(DomainError):
    status_code = 422
    title = "Weak Password"


def _current_period_year() -> int:
    """Academic year starting in September."""
    now = datetime.now(tz=UTC)
    return now.year if now.month >= 9 else now.year - 1


async def register(
    db: AsyncSession,
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    ieee_membership_number: str,
    ieee_grade: str | None = None,
    university: str = "University of Oulu",
    study_level: str | None = None,
    study_program: str | None = None,
    expected_graduation_year: int | None = None,
    profile_visibility: Visibility = Visibility.private,
    consents: dict[str, Any],
) -> User | None:
    """Register a new user. Returns None if email already taken (no enumeration)."""
    if not consents.get("privacy") or not consents.get("terms"):
        raise DomainError("Privacy and terms consent are required.")

    if await is_password_breached(password):
        raise WeakPasswordError(
            "This password has appeared in a data breach. Please choose another."
        )

    existing = await get_by_email(db, email)
    if existing is not None:
        return None

    user = User(
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        ieee_membership_number=ieee_membership_number,
        ieee_grade=ieee_grade,
        university=university,
        study_level=study_level,
        study_program=study_program,
        expected_graduation_year=expected_graduation_year,
        profile_visibility=profile_visibility,
        consents=consents,
        status=UserStatus.pending_email,
    )
    db.add(user)
    await db.flush()

    period = MembershipPeriod(
        user_id=user.id,
        period_year=_current_period_year(),
        ieee_membership_number=ieee_membership_number,
        status=MembershipStatus.pending,
    )
    db.add(period)

    raw, token_hash = generate_token()
    et = EmailToken(
        user_id=user.id,
        kind=EmailTokenKind.email_verify,
        token_hash=token_hash,
        expires_at=datetime.now(tz=UTC) + timedelta(hours=24),
    )
    db.add(et)
    await db.flush()

    settings = get_settings()
    verify_url = f"{settings.public_base_url}/auth/verify-email?token={raw}"
    html, text = render(
        "email_verify",
        first_name=first_name,
        verify_url=verify_url,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=email,
            subject="Verify your email - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )

    return user


async def login(
    db: AsyncSession,
    *,
    email: str,
    password: str,
) -> User:
    """Authenticate a user by email+password. Raises on failure."""
    user = await get_by_email(db, email)
    if user is None:
        verify_dummy(password)
        raise AuthenticationError("Invalid credentials.")

    if not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid credentials.")

    if user.status == UserStatus.suspended:
        raise AuthenticationError("Invalid credentials.")

    if needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)

    return user


async def verify_email(db: AsyncSession, *, raw_token: str) -> User:
    """Consume a verification token and advance user status."""
    h = hash_token(raw_token)
    stmt = select(EmailToken).where(
        EmailToken.token_hash == h,
        EmailToken.kind == EmailTokenKind.email_verify,
        EmailToken.used_at.is_(None),
    )
    token = (await db.execute(stmt)).scalar_one_or_none()
    if token is None:
        raise AuthenticationError("Invalid or expired verification token.")

    if token.expires_at < datetime.now(tz=UTC):
        raise AuthenticationError("Verification token has expired.")

    token.used_at = datetime.now(tz=UTC)

    user = await db.get(User, token.user_id)
    if user is None:
        raise AuthenticationError("User not found.")

    if user.status == UserStatus.pending_email:
        user.status = UserStatus.pending_approval
        user.email_verified_at = datetime.now(tz=UTC)

        settings = get_settings()
        html, text = render(
            "welcome_pending_approval",
            first_name=user.first_name,
            base_url=settings.public_base_url,
        )
        await get_backend().send(
            EmailMessage(
                to=user.email,
                subject="Application submitted - IEEE SB Oulu",
                html=html,
                text=text,
            )
        )

    return user


async def resend_verification(db: AsyncSession, *, email: str) -> None:
    """Resend verification email. Always returns success (no enumeration)."""
    user = await get_by_email(db, email)
    if user is None or user.status != UserStatus.pending_email:
        return

    raw, token_hash = generate_token()
    et = EmailToken(
        user_id=user.id,
        kind=EmailTokenKind.email_verify,
        token_hash=token_hash,
        expires_at=datetime.now(tz=UTC) + timedelta(hours=24),
    )
    db.add(et)
    await db.flush()

    settings = get_settings()
    verify_url = f"{settings.public_base_url}/auth/verify-email?token={raw}"
    html, text = render(
        "email_verify",
        first_name=user.first_name,
        verify_url=verify_url,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=user.email,
            subject="Verify your email - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )


async def forgot_password(db: AsyncSession, *, email: str) -> None:
    """Send password reset email. Always returns success (no enumeration)."""
    user = await get_by_email(db, email)
    if user is None:
        return

    raw, token_hash = generate_token()
    et = EmailToken(
        user_id=user.id,
        kind=EmailTokenKind.password_reset,
        token_hash=token_hash,
        expires_at=datetime.now(tz=UTC) + timedelta(hours=1),
    )
    db.add(et)
    await db.flush()

    settings = get_settings()
    reset_url = f"{settings.public_base_url}/auth/reset-password?token={raw}"
    html, text = render(
        "password_reset",
        first_name=user.first_name,
        reset_url=reset_url,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=user.email,
            subject="Reset your password - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )


async def reset_password(db: AsyncSession, *, raw_token: str, new_password: str) -> User:
    """Consume a reset token and change the password."""
    if await is_password_breached(new_password):
        raise WeakPasswordError(
            "This password has appeared in a data breach. Please choose another."
        )

    h = hash_token(raw_token)
    stmt = select(EmailToken).where(
        EmailToken.token_hash == h,
        EmailToken.kind == EmailTokenKind.password_reset,
        EmailToken.used_at.is_(None),
    )
    token = (await db.execute(stmt)).scalar_one_or_none()
    if token is None:
        raise AuthenticationError("Invalid or expired reset token.")

    if token.expires_at < datetime.now(tz=UTC):
        raise AuthenticationError("Reset token has expired.")

    token.used_at = datetime.now(tz=UTC)

    user = await db.get(User, token.user_id)
    if user is None:
        raise AuthenticationError("User not found.")

    user.password_hash = hash_password(new_password)

    settings = get_settings()
    html, text = render(
        "password_changed",
        first_name=user.first_name,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=user.email,
            subject="Password changed - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )

    return user


async def change_password(
    db: AsyncSession,
    *,
    user: User,
    current_password: str,
    new_password: str,
) -> None:
    """Change password for an authenticated user."""
    if not verify_password(current_password, user.password_hash):
        raise AuthenticationError("Current password is incorrect.")

    if await is_password_breached(new_password):
        raise WeakPasswordError(
            "This password has appeared in a data breach. Please choose another."
        )

    user.password_hash = hash_password(new_password)

    settings = get_settings()
    html, text = render(
        "password_changed",
        first_name=user.first_name,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=user.email,
            subject="Password changed - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )


async def renew_membership(db: AsyncSession, *, user: User) -> MembershipPeriod:
    """Create a renewal for the current academic year. Low friction — reuses existing data."""
    year = _current_period_year()

    existing = (
        await db.execute(
            select(MembershipPeriod).where(
                MembershipPeriod.user_id == user.id,
                MembershipPeriod.period_year == year,
            )
        )
    ).scalar_one_or_none()

    if existing is not None:
        raise ConflictError(f"You already have a membership application for {year}-{year + 1}.")

    period = MembershipPeriod(
        user_id=user.id,
        period_year=year,
        ieee_membership_number=user.ieee_membership_number,
        status=MembershipStatus.pending,
    )
    db.add(period)

    if user.status == UserStatus.active:
        user.status = UserStatus.pending_approval

    return period
