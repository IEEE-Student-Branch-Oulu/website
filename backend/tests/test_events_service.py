"""Pure-logic tests for the events service — no database required."""

from datetime import UTC, datetime

from app.domains.events.service import derive_spots_left, derive_status, format_display


class TestDeriveStatus:
    def test_upcoming(self) -> None:
        now = datetime(2026, 3, 1, tzinfo=UTC)
        starts = datetime(2026, 3, 15, tzinfo=UTC)
        assert derive_status(starts, None, now) == "upcoming"

    def test_past_with_no_end(self) -> None:
        now = datetime(2026, 3, 16, tzinfo=UTC)
        starts = datetime(2026, 3, 15, tzinfo=UTC)
        assert derive_status(starts, None, now) == "past"

    def test_past_with_end(self) -> None:
        now = datetime(2026, 3, 16, tzinfo=UTC)
        starts = datetime(2026, 3, 15, 11, tzinfo=UTC)
        ends = datetime(2026, 3, 15, 15, tzinfo=UTC)
        assert derive_status(starts, ends, now) == "past"

    def test_ongoing(self) -> None:
        now = datetime(2026, 3, 15, 13, tzinfo=UTC)
        starts = datetime(2026, 3, 15, 11, tzinfo=UTC)
        ends = datetime(2026, 3, 15, 15, tzinfo=UTC)
        assert derive_status(starts, ends, now) == "ongoing"


class TestDeriveSpotsLeft:
    def test_no_capacity(self) -> None:
        assert derive_spots_left(None, 5) is None

    def test_capacity_minus_attendees(self) -> None:
        assert derive_spots_left(30, 7) == 23

    def test_clamped_at_zero(self) -> None:
        assert derive_spots_left(10, 99) == 0


class TestFormatDisplay:
    def test_same_day(self) -> None:
        starts = datetime(2026, 3, 15, 11, tzinfo=UTC)  # 13:00 EET
        ends = datetime(2026, 3, 15, 15, tzinfo=UTC)
        date_disp, time_disp = format_display(starts, ends, "Europe/Helsinki")
        assert date_disp == "Sun, Mar 15, 2026"
        assert "13:00" in time_disp and "17:00" in time_disp

    def test_no_end_time(self) -> None:
        starts = datetime(2026, 3, 15, 11, tzinfo=UTC)
        _, time_disp = format_display(starts, None, "Europe/Helsinki")
        assert time_disp.startswith("13:00")

    def test_multi_day(self) -> None:
        starts = datetime(2025, 11, 1, 8, tzinfo=UTC)
        ends = datetime(2025, 11, 2, 8, tzinfo=UTC)
        _, time_disp = format_display(starts, ends, "Europe/Helsinki")
        assert "Nov 2" in time_disp
