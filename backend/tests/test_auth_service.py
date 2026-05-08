"""Tests for auth service — register, login, verify, password flows, renewal.

These require a database (TEST_DATABASE_URL). They test the service layer
directly, not HTTP endpoints, so they exercise business logic without
routing/middleware concerns.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import EmailToken, EmailTokenKind
from app.auth.service import (
    WeakPasswordError,
    _current_period_year,
    change_password,
    forgot_password,
    login,
    register,
    renew_membership,
    resend_verification,
    reset_password,
    verify_email,
)
from app.auth.tokens import generate_token, hash_token
from app.core.email import MemoryBackend, configure_backend, get_backend
from app.core.errors import AuthenticationError, ConflictError
from app.domains.members.models import (
    MembershipPeriod,
    MembershipStatus,
    User,
    UserStatus,
    Visibility,
)
from tests.conftest import needs_db

_CONSENTS = {"privacy": True, "terms": True}
_STRONG_PW = "correct-horse-battery-staple"


@pytest.fixture(autouse=True)
def _use_memory_email() -> None:
    configure_backend(MemoryBackend())


def _email_backend() -> MemoryBackend:
    backend = get_backend()
    assert isinstance(backend, MemoryBackend)
    return backend


async def _register_alice(db: AsyncSession) -> User:
    user = await register(
        db,
        email="alice@example.com",
        password=_STRONG_PW,
        first_name="Alice",
        last_name="Smith",
        ieee_membership_number="12345678",
        consents=_CONSENTS,
    )
    assert user is not None
    await db.flush()
    return user


class TestCurrentPeriodYear:
    def test_september_onwards_is_current_year(self) -> None:
        with patch("app.auth.service.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2025, 9, 1, tzinfo=UTC)
            assert _current_period_year() == 2025

    def test_before_september_is_previous_year(self) -> None:
        with patch("app.auth.service.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2025, 3, 15, tzinfo=UTC)
            assert _current_period_year() == 2024


@needs_db
class TestRegister:
    async def test_creates_user_with_pending_email_status(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        assert user.status == UserStatus.pending_email
        assert user.email == "alice@example.com"

    async def test_creates_membership_period(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        period = (
            await db_session.execute(
                select(MembershipPeriod).where(MembershipPeriod.user_id == user.id)
            )
        ).scalar_one()
        assert period.status == MembershipStatus.pending

    async def test_sends_verification_email(self, db_session: AsyncSession) -> None:
        await _register_alice(db_session)
        backend = _email_backend()
        assert len(backend.outbox) == 1
        assert "verify" in backend.outbox[0].subject.lower()

    async def test_creates_email_verification_token(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        token = (
            await db_session.execute(
                select(EmailToken).where(
                    EmailToken.user_id == user.id,
                    EmailToken.kind == EmailTokenKind.email_verify,
                )
            )
        ).scalar_one()
        assert token.used_at is None
        assert token.expires_at > datetime.now(tz=UTC)

    async def test_duplicate_email_returns_none(self, db_session: AsyncSession) -> None:
        await _register_alice(db_session)
        await db_session.flush()
        result = await register(
            db_session,
            email="alice@example.com",
            password=_STRONG_PW,
            first_name="Bob",
            last_name="Jones",
            ieee_membership_number="87654321",
            consents=_CONSENTS,
        )
        assert result is None

    async def test_missing_consent_rejected(self, db_session: AsyncSession) -> None:
        from app.core.errors import DomainError

        with pytest.raises(DomainError, match="consent"):
            await register(
                db_session,
                email="bob@example.com",
                password=_STRONG_PW,
                first_name="Bob",
                last_name="Jones",
                ieee_membership_number="87654321",
                consents={"privacy": False, "terms": True},
            )

    async def test_breached_password_rejected(self, db_session: AsyncSession) -> None:
        with pytest.raises(WeakPasswordError, match="breach"):
            await register(
                db_session,
                email="bob@example.com",
                password="password",
                first_name="Bob",
                last_name="Jones",
                ieee_membership_number="87654321",
                consents=_CONSENTS,
            )

    async def test_profile_visibility_saved(self, db_session: AsyncSession) -> None:
        user = await register(
            db_session,
            email="vis@example.com",
            password=_STRONG_PW,
            first_name="Vis",
            last_name="User",
            ieee_membership_number="99999999",
            consents=_CONSENTS,
            profile_visibility=Visibility.public,
        )
        assert user is not None
        assert user.profile_visibility == Visibility.public


@needs_db
class TestLogin:
    async def test_valid_credentials(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.active
        await db_session.flush()
        result = await login(db_session, email="alice@example.com", password=_STRONG_PW)
        assert result.id == user.id

    async def test_wrong_password(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.active
        await db_session.flush()
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await login(db_session, email="alice@example.com", password="wrong-password!!")

    async def test_unknown_email(self, db_session: AsyncSession) -> None:
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await login(db_session, email="nobody@example.com", password=_STRONG_PW)

    async def test_suspended_user_rejected(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.suspended
        await db_session.flush()
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await login(db_session, email="alice@example.com", password=_STRONG_PW)


@needs_db
class TestVerifyEmail:
    async def test_advances_to_pending_approval(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        await db_session.flush()
        token = (
            await db_session.execute(
                select(EmailToken).where(
                    EmailToken.user_id == user.id,
                    EmailToken.kind == EmailTokenKind.email_verify,
                )
            )
        ).scalar_one()

        raw, _ = generate_token()
        token.token_hash = hash_token(raw)
        await db_session.flush()

        result = await verify_email(db_session, raw_token=raw)
        assert result.status == UserStatus.pending_approval
        assert result.email_verified_at is not None

    async def test_expired_token_rejected(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        await db_session.flush()

        raw, h = generate_token()
        expired_token = EmailToken(
            user_id=user.id,
            kind=EmailTokenKind.email_verify,
            token_hash=h,
            expires_at=datetime.now(tz=UTC) - timedelta(hours=1),
        )
        db_session.add(expired_token)
        await db_session.flush()

        with pytest.raises(AuthenticationError, match="expired"):
            await verify_email(db_session, raw_token=raw)

    async def test_invalid_token_rejected(self, db_session: AsyncSession) -> None:
        with pytest.raises(AuthenticationError, match="Invalid"):
            await verify_email(db_session, raw_token="bogus-token")

    async def test_sends_pending_approval_email(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        await db_session.flush()

        token = (
            await db_session.execute(
                select(EmailToken).where(
                    EmailToken.user_id == user.id,
                    EmailToken.kind == EmailTokenKind.email_verify,
                )
            )
        ).scalar_one()
        raw, _ = generate_token()
        token.token_hash = hash_token(raw)
        await db_session.flush()

        _email_backend().outbox.clear()
        await verify_email(db_session, raw_token=raw)
        assert any(
            "submitted" in m.subject.lower() or "pending" in m.subject.lower()
            for m in _email_backend().outbox
        )


@needs_db
class TestResendVerification:
    async def test_resend_for_pending_email_user(self, db_session: AsyncSession) -> None:
        await _register_alice(db_session)
        await db_session.flush()
        _email_backend().outbox.clear()
        await resend_verification(db_session, email="alice@example.com")
        assert len(_email_backend().outbox) == 1

    async def test_resend_for_nonexistent_email_does_not_error(
        self, db_session: AsyncSession
    ) -> None:
        await resend_verification(db_session, email="nobody@example.com")


@needs_db
class TestForgotPassword:
    async def test_sends_reset_email(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.active
        await db_session.flush()
        _email_backend().outbox.clear()
        await forgot_password(db_session, email="alice@example.com")
        assert len(_email_backend().outbox) == 1
        assert "reset" in _email_backend().outbox[0].subject.lower()

    async def test_nonexistent_email_does_not_error(self, db_session: AsyncSession) -> None:
        await forgot_password(db_session, email="nobody@example.com")


@needs_db
class TestResetPassword:
    async def test_changes_password(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.active
        await db_session.flush()

        raw, h = generate_token()
        db_session.add(
            EmailToken(
                user_id=user.id,
                kind=EmailTokenKind.password_reset,
                token_hash=h,
                expires_at=datetime.now(tz=UTC) + timedelta(hours=1),
            )
        )
        await db_session.flush()

        new_pw = "new-strong-password-99"
        result = await reset_password(db_session, raw_token=raw, new_password=new_pw)
        assert result.id == user.id

    async def test_expired_reset_token_rejected(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        await db_session.flush()

        raw, h = generate_token()
        db_session.add(
            EmailToken(
                user_id=user.id,
                kind=EmailTokenKind.password_reset,
                token_hash=h,
                expires_at=datetime.now(tz=UTC) - timedelta(hours=1),
            )
        )
        await db_session.flush()

        with pytest.raises(AuthenticationError, match="expired"):
            await reset_password(db_session, raw_token=raw, new_password="new-strong-password-99")

    async def test_breached_new_password_rejected(self, db_session: AsyncSession) -> None:
        with pytest.raises(WeakPasswordError):
            await reset_password(db_session, raw_token="anything", new_password="password")


@needs_db
class TestChangePassword:
    async def test_valid_change(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.active
        await db_session.flush()
        _email_backend().outbox.clear()
        await change_password(
            db_session, user=user, current_password=_STRONG_PW, new_password="another-strong-pw-99"
        )
        assert any("changed" in m.subject.lower() for m in _email_backend().outbox)

    async def test_wrong_current_password(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        await db_session.flush()
        with pytest.raises(AuthenticationError, match="incorrect"):
            await change_password(
                db_session,
                user=user,
                current_password="wrong!!!!!!!!",
                new_password="new-pw-12345678",
            )


@needs_db
class TestRenewMembership:
    async def test_creates_renewal_period(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.active
        await db_session.flush()

        existing = (
            await db_session.execute(
                select(MembershipPeriod).where(MembershipPeriod.user_id == user.id)
            )
        ).scalar_one()
        existing.period_year = 2020
        await db_session.flush()

        period = await renew_membership(db_session, user=user)
        assert period.status == MembershipStatus.pending
        assert period.ieee_membership_number == user.ieee_membership_number

    async def test_duplicate_year_raises_conflict(self, db_session: AsyncSession) -> None:
        user = await _register_alice(db_session)
        user.status = UserStatus.active
        await db_session.flush()

        with pytest.raises(ConflictError, match="already"):
            await renew_membership(db_session, user=user)
