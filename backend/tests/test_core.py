"""Tests for utilities in app/core/."""

from app.core.errors import NotFoundError
from app.core.slug import slugify


class TestSlugify:
    def test_basic(self) -> None:
        assert slugify("Hello World") == "hello-world"

    def test_punctuation_stripped(self) -> None:
        assert slugify("How We Built a Working Radar System!") == (
            "how-we-built-a-working-radar-system"
        )

    def test_max_length_word_boundary(self) -> None:
        # word boundary should keep slugs readable, not mid-word truncations
        result = slugify("a" * 200)
        assert len(result) <= 80


class TestNotFoundError:
    def test_default_detail_is_title(self) -> None:
        err = NotFoundError()
        assert err.status_code == 404
        assert err.detail == "Not Found"

    def test_custom_detail(self) -> None:
        err = NotFoundError("Event 'foo' not found.")
        assert err.detail == "Event 'foo' not found."
