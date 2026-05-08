"""Tests for auth utility modules: passwords, tokens, sessions, csrf, email, audit."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.auth.passwords import (
    DUMMY_HASH,
    hash_password,
    is_password_breached,
    needs_rehash,
    verify_dummy,
    verify_password,
)
from app.auth.tokens import generate_token, hash_token


class TestPasswords:
    def test_hash_and_verify(self) -> None:
        pw = "my-secure-password-12345"
        h = hash_password(pw)
        assert h != pw
        assert verify_password(pw, h)

    def test_wrong_password(self) -> None:
        h = hash_password("correct-horse-battery-staple")
        assert not verify_password("wrong-password-here!", h)

    def test_needs_rehash_with_current_params(self) -> None:
        h = hash_password("test-password-here")
        assert not needs_rehash(h)

    def test_verify_dummy_does_not_raise(self) -> None:
        verify_dummy("anything-goes-here")

    def test_dummy_hash_is_valid_argon2(self) -> None:
        assert DUMMY_HASH.startswith("$argon2id$")


class TestHIBP:
    @pytest.mark.anyio
    async def test_breached_password_detected(self) -> None:
        result = await is_password_breached("password")
        assert result is True

    @pytest.mark.anyio
    async def test_network_error_fails_open(self) -> None:
        import httpx

        with patch("app.auth.passwords.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.get.side_effect = httpx.ConnectError("offline")
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_cls.return_value = mock_client
            result = await is_password_breached("some-password")
            assert result is False


class TestTokens:
    def test_generate_returns_pair(self) -> None:
        raw, h = generate_token()
        assert len(raw) > 20
        assert len(h) == 64
        assert hash_token(raw) == h

    def test_tokens_are_unique(self) -> None:
        tokens = {generate_token()[0] for _ in range(10)}
        assert len(tokens) == 10

    def test_hash_token_deterministic(self) -> None:
        assert hash_token("test") == hash_token("test")
        assert hash_token("a") != hash_token("b")
