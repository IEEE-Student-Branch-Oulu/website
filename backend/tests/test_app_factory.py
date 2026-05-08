"""Tests for the application factory and email backend configuration."""

from __future__ import annotations

from app.config import Settings
from app.core.email import ConsoleBackend, ResendBackend, get_backend
from app.main import _configure_email


class TestConfigureEmail:
    def test_console_backend_by_default(self) -> None:
        s = Settings(email_backend="console")
        _configure_email(s)
        assert isinstance(get_backend(), ConsoleBackend)

    def test_resend_backend_with_key(self) -> None:
        s = Settings(email_backend="resend", email_resend_api_key="re_test_123")
        _configure_email(s)
        assert isinstance(get_backend(), ResendBackend)

    def test_resend_without_key_falls_back_to_console(self, caplog: object) -> None:
        s = Settings(email_backend="resend", email_resend_api_key="")
        _configure_email(s)
        assert isinstance(get_backend(), ConsoleBackend)


class TestCreateApp:
    def test_app_creates_successfully(self) -> None:
        from app.main import create_app

        app = create_app()
        assert app.title == "IEEE SB Oulu API"

    def test_app_has_expected_routes(self) -> None:
        from app.main import create_app

        app = create_app()
        paths = {r.path for r in app.routes if hasattr(r, "path")}
        assert "/api/v1/healthz" in paths
        assert "/api/v1/auth/login" in paths
        assert "/api/v1/admin/users" in paths
        assert "/api/v1/members/" in paths
