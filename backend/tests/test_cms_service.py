"""Pure-logic tests for CMS authoring helpers (no DB needed)."""

from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

import pytest

from app.core import storage
from app.domains.events.models import Event
from app.domains.events.service import _to_utc, to_read
from app.domains.posts.models import Post
from app.domains.posts.service import _initials, _read_minutes, to_meta


class TestReadMinutes:
    def test_minimum_one_minute(self) -> None:
        assert _read_minutes("a few words") == 1

    def test_scales_with_word_count(self) -> None:
        assert _read_minutes(" ".join(["word"] * 400)) == 2


class TestInitials:
    def test_two_names(self) -> None:
        assert _initials("Ada Lovelace") == "AL"

    def test_single_name(self) -> None:
        assert _initials("Ada") == "A"

    def test_empty_falls_back(self) -> None:
        assert _initials("") == "?"


class TestToMetaNewFields:
    def test_cover_and_event_slug_mapped(self) -> None:
        post = Post(
            id=1,
            title="Recap",
            slug="recap",
            excerpt="ex",
            body_md="text",
            category="event-recap",
            author_name="A B",
            author_initials="AB",
            author_role="Member",
            published_on=date(2026, 2, 12),
            read_minutes=3,
            tags=[],
            featured=False,
            cover_image_url="https://cdn/x.jpg",
            event_slug="past-event",
        )
        meta = to_meta(post)
        assert meta.cover_image_url == "https://cdn/x.jpg"
        assert meta.event_slug == "past-event"


class TestEventToUtc:
    def test_naive_interpreted_in_branch_tz(self) -> None:
        # 12:00 Helsinki summer time == 09:00 UTC
        result = _to_utc(datetime(2026, 7, 1, 12, 0))
        assert result.tzinfo == UTC
        assert result.hour == 9

    def test_aware_converted(self) -> None:
        aware = datetime(2026, 7, 1, 12, 0, tzinfo=ZoneInfo("Europe/Helsinki"))
        assert _to_utc(aware).hour == 9


class TestEventToReadCover:
    def test_cover_image_mapped(self) -> None:
        event = Event(
            id=1,
            title="T",
            slug="t",
            description="d",
            starts_at=datetime(2026, 7, 1, 9, 0, tzinfo=UTC),
            ends_at=None,
            location="Oulu",
            type="workshop",
            attendees_count=0,
            is_highlighted=False,
            tags=[],
            cover_image_url="https://cdn/e.jpg",
        )
        assert to_read(event).cover_image_url == "https://cdn/e.jpg"


class TestStorageValidation:
    def test_rejects_unsupported_type(self) -> None:
        with pytest.raises(storage.StorageError):
            storage.upload(b"x", "application/pdf")

    def test_rejects_oversize(self) -> None:
        with pytest.raises(storage.StorageError):
            storage.upload(b"x" * (storage.MAX_BYTES + 1), "image/png")
