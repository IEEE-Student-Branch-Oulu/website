"""Tests for application settings."""

from __future__ import annotations

from app.config import Settings


class TestSettings:
    def test_cors_origin_list_splits_commas(self) -> None:
        s = Settings(cors_origins="http://a.com, http://b.com")
        assert s.cors_origin_list == ["http://a.com", "http://b.com"]

    def test_cors_origin_list_single(self) -> None:
        s = Settings(cors_origins="http://localhost:3000")
        assert s.cors_origin_list == ["http://localhost:3000"]

    def test_cors_origin_list_strips_whitespace(self) -> None:
        s = Settings(cors_origins="  http://a.com  ,  http://b.com  ")
        assert all(not o.startswith(" ") for o in s.cors_origin_list)

    def test_is_dev_true_for_dev(self) -> None:
        s = Settings(env="dev")
        assert s.is_dev is True

    def test_is_dev_false_for_prod(self) -> None:
        s = Settings(env="prod")
        assert s.is_dev is False

    def test_defaults(self) -> None:
        s = Settings(_env_file=None)
        assert s.email_backend == "console"
        assert s.timezone == "Europe/Helsinki"
