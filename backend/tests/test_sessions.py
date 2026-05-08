"""Tests for session helpers: cookie management and utility functions."""

from __future__ import annotations

from starlette.responses import Response

from app.auth.sessions import (
    COOKIE_NAME,
    SESSION_ABSOLUTE_DAYS,
    SESSION_IDLE_DAYS,
    _truncate,
    delete_session_cookie,
    set_session_cookie,
)


class TestSessionCookie:
    def test_set_cookie_applies_security_flags(self) -> None:
        resp = Response()
        set_session_cookie(resp, "tok-123", secure=True)
        raw = resp.headers.get("set-cookie", "")
        assert COOKIE_NAME in raw
        assert "httponly" in raw.lower()
        assert "secure" in raw.lower()
        assert "samesite=lax" in raw.lower()

    def test_set_cookie_insecure_mode(self) -> None:
        resp = Response()
        set_session_cookie(resp, "tok-123", secure=False)
        raw = resp.headers.get("set-cookie", "")
        assert "secure" not in raw.lower().replace("samesite", "")

    def test_set_cookie_max_age_matches_idle_days(self) -> None:
        resp = Response()
        set_session_cookie(resp, "tok", secure=True)
        raw = resp.headers.get("set-cookie", "")
        expected = str(60 * 60 * 24 * SESSION_IDLE_DAYS)
        assert expected in raw

    def test_delete_cookie(self) -> None:
        resp = Response()
        delete_session_cookie(resp, secure=True)
        raw = resp.headers.get("set-cookie", "")
        assert COOKIE_NAME in raw
        assert "max-age=0" in raw.lower() or '"0"' in raw


class TestTruncate:
    def test_none_returns_none(self) -> None:
        assert _truncate(None, 10) is None

    def test_short_string_unchanged(self) -> None:
        assert _truncate("hello", 10) == "hello"

    def test_long_string_truncated(self) -> None:
        assert _truncate("a" * 300, 255) == "a" * 255

    def test_exact_length(self) -> None:
        assert _truncate("abc", 3) == "abc"


class TestConstants:
    def test_idle_days_less_than_absolute(self) -> None:
        assert SESSION_IDLE_DAYS < SESSION_ABSOLUTE_DAYS

    def test_cookie_name(self) -> None:
        assert COOKIE_NAME == "ieee_sid"
