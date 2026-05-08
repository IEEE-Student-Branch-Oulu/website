"""Tests for email backends and template rendering."""

from __future__ import annotations

import pytest

from app.core.email import (
    ConsoleBackend,
    EmailMessage,
    MemoryBackend,
    configure_backend,
    get_backend,
    render,
)


def _msg() -> EmailMessage:
    return EmailMessage(
        to="test@example.com",
        subject="Test",
        html="<p>hi</p>",
        text="hi",
    )


class TestMemoryBackend:
    @pytest.mark.anyio
    async def test_stores_messages(self) -> None:
        backend = MemoryBackend()
        msg = _msg()
        await backend.send(msg)
        assert len(backend.outbox) == 1
        assert backend.outbox[0].to == "test@example.com"

    @pytest.mark.anyio
    async def test_multiple_messages(self) -> None:
        backend = MemoryBackend()
        await backend.send(_msg())
        await backend.send(_msg())
        assert len(backend.outbox) == 2


class TestConsoleBackend:
    @pytest.mark.anyio
    async def test_does_not_raise(self) -> None:
        backend = ConsoleBackend()
        await backend.send(_msg())


class TestBackendConfig:
    def test_configure_and_get(self) -> None:
        mem = MemoryBackend()
        configure_backend(mem)
        assert get_backend() is mem
        configure_backend(ConsoleBackend())


class TestTemplateRendering:
    def test_email_verify_renders(self) -> None:
        html, text = render(
            "email_verify",
            first_name="Alice",
            verify_url="https://example.com/verify?token=abc",
            base_url="https://example.com",
        )
        assert "Alice" in html
        assert "verify?token=abc" in html
        assert "Alice" in text
        assert "verify?token=abc" in text

    def test_password_reset_renders(self) -> None:
        html, text = render(
            "password_reset",
            first_name="Bob",
            reset_url="https://example.com/reset?token=xyz",
            base_url="https://example.com",
        )
        assert "Bob" in html
        assert "1 hour" in text

    def test_application_approved_renders(self) -> None:
        html, text = render(
            "application_approved",
            first_name="Carol",
            period_year=2026,
            base_url="https://example.com",
        )
        assert "2026-2027" in html
        assert "Carol" in text

    def test_application_rejected_with_reason(self) -> None:
        html, text = render(
            "application_rejected",
            first_name="Dave",
            period_year=2026,
            reason="Missing IEEE number",
            base_url="https://example.com",
        )
        assert "Missing IEEE number" in html
        assert "Missing IEEE number" in text

    def test_application_rejected_without_reason(self) -> None:
        html, _ = render(
            "application_rejected",
            first_name="Eve",
            period_year=2026,
            reason=None,
            base_url="https://example.com",
        )
        assert "Eve" in html
