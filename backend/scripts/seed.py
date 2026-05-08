"""Seed development data.

Idempotent: re-running inserts only rows whose `slug` doesn't yet exist.
Run with `make seed` or `uv run python -m scripts.seed`.
"""

import asyncio
from datetime import UTC, date, datetime
from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionLocal
from app.domains.events.models import Event
from app.domains.posts.models import Post

_M = TypeVar("_M", Event, Post)

EVENTS: list[dict[str, Any]] = [
    {
        "title": "AI & Machine Learning Workshop",
        "slug": "ai-ml-workshop-march-2026",
        "description": (
            "A hands-on introduction to ML fundamentals. Train a real classifier "
            "from scratch using Python and scikit-learn. No prior ML experience "
            "required — just bring a laptop with Python installed."
        ),
        "starts_at": datetime(2026, 3, 15, 11, 0, tzinfo=UTC),
        "ends_at": datetime(2026, 3, 15, 15, 0, tzinfo=UTC),
        "location": "Linnanmaa Campus, Room TS101",
        "location_url": "https://maps.google.com/?q=University+of+Oulu",
        "type": "workshop",
        "rsvp_link": "https://forms.gle/placeholder",
        "capacity": 30,
        "attendees_count": 23,
        "tags": ["Python", "ML", "scikit-learn"],
        "is_highlighted": True,
    },
    {
        "title": "Spring General Meeting 2026",
        "slug": "spring-general-meeting-2026",
        "description": (
            "Our spring general meeting. Agenda: board activity reports, budget "
            "overview, summer plans, and open floor for member proposals. Free "
            "pizza after."
        ),
        "starts_at": datetime(2026, 3, 22, 15, 0, tzinfo=UTC),
        "ends_at": datetime(2026, 3, 22, 17, 0, tzinfo=UTC),
        "location": "Linnanmaa Campus, Room L2",
        "type": "meeting",
        "rsvp_link": "https://forms.gle/placeholder",
        "tags": ["Official", "Open to all"],
    },
    {
        "title": "Game Night & Social Mixer",
        "slug": "game-night-april-2026",
        "description": (
            "Decompress from the thesis grind. Board games, video games, and good "
            "people. No agenda, no slides. Just show up."
        ),
        "starts_at": datetime(2026, 4, 4, 15, 0, tzinfo=UTC),
        "ends_at": datetime(2026, 4, 4, 19, 0, tzinfo=UTC),
        "location": "OTK Student Club, Linnanmaa",
        "type": "social",
        "tags": ["Free", "Casual"],
    },
    {
        "title": "GNU Radio & SDR Workshop",
        "slug": "gnu-radio-sdr-workshop-feb-2026",
        "description": (
            "Built a working radar system with a $20 RTL-SDR dongle and GNU Radio. "
            "18 attendees went from zero to detecting passing cars in four hours."
        ),
        "starts_at": datetime(2026, 2, 8, 11, 0, tzinfo=UTC),
        "ends_at": datetime(2026, 2, 8, 15, 0, tzinfo=UTC),
        "location": "Linnanmaa Campus, Room TS101",
        "type": "workshop",
        "tags": ["SDR", "GNU Radio", "RF"],
    },
    {
        "title": "Embedded Systems Hackathon",
        "slug": "embedded-hackathon-nov-2025",
        "description": (
            "24-hour hackathon focused on embedded systems. Teams of 2–3 built "
            "projects using STM32 boards. Winner built an autonomous "
            "plant-watering system."
        ),
        "starts_at": datetime(2025, 11, 1, 8, 0, tzinfo=UTC),
        "ends_at": datetime(2025, 11, 2, 8, 0, tzinfo=UTC),
        "location": "Linnanmaa Campus, Fab Lab",
        "type": "hackathon",
        "tags": ["STM32", "24h", "Hardware"],
        "is_highlighted": True,
    },
]


POSTS: list[dict[str, Any]] = [
    {
        "title": "How We Built a Working Radar System with a $20 SDR Dongle and GNU Radio",
        "slug": "gnu-radio-sdr-radar-workshop",
        "excerpt": (
            "Eighteen students, one afternoon, zero prior radar experience. "
            "Here's how we turned cheap hardware and open-source signal processing "
            "into a working object detection system."
        ),
        "body_md": (
            "## Background\n\n"
            "Radar sounds like expensive defence hardware. With a cheap RTL-SDR "
            "dongle and GNU Radio, it isn't.\n\n"
            "## The Hardware Stack\n\n"
            "Per station: RTL-SDR v3 (€18), two patch antennas (€3), an SMA "
            "adapter, and a laptop running Linux.\n\n"
            "### RTL-SDR: What it Actually Is\n\n"
            "A USB DVB-T tuner that, in raw sampling mode, becomes a wideband "
            "SDR receiver covering ~24 MHz – 1.766 GHz.\n\n"
            "## Results\n\n"
            "Hand motion at 2 m, directional, with approximate speed. "
            "Range and multi-target detection were out of scope.\n"
        ),
        "category": "workshop-recap",
        "author_name": "Juhani Virtanen",
        "author_initials": "JV",
        "author_role": "Technical Officer",
        "published_on": date(2026, 2, 12),
        "read_minutes": 9,
        "tags": ["SDR", "GNU Radio", "RF", "Python", "Workshop"],
        "featured": True,
    },
    {
        "title": "IEEE Oulu Wins Best Student Branch Activity Award",
        "slug": "ieee-oulu-best-activity-award-2025",
        "excerpt": (
            "At the IEEE Finland Section Annual Meeting in Helsinki, the Oulu "
            "Student Branch was recognised for outstanding technical activity "
            "and membership growth in 2025."
        ),
        "body_md": (
            "## What We Submitted\n\nA portfolio of workshops, talks, and "
            "industry visits across the year.\n\n## What It Means\n\nMore "
            "support, more visibility, and a clearer path for future boards.\n"
        ),
        "category": "branch-news",
        "author_name": "IEEE Oulu Board",
        "author_initials": "IB",
        "author_role": "Executive Board",
        "published_on": date(2026, 2, 1),
        "read_minutes": 4,
        "tags": ["IEEE Finland", "Award", "Announcement"],
    },
    {
        "title": "6G Is Not Just Faster 5G — Notes from the Nokia Bell Labs Talk",
        "slug": "6g-nokia-tech-talk-notes",
        "excerpt": (
            "Dr. Aino Mäkinen's talk dismantled a lot of assumptions. 6G isn't "
            "about raw throughput — it's about sensing, positioning, and AI."
        ),
        "body_md": (
            "## Sensing as a First-Class Citizen\n\nThe radio itself is a "
            "sensor.\n\n## Native AI Integration\n\nBaseband decisions made "
            "with on-device models, not handed off.\n\n### What This Means "
            "for Theses\n\nPlenty of open problems if you're looking.\n"
        ),
        "category": "tech-notes",
        "author_name": "Aleksi Heikkinen",
        "author_initials": "AH",
        "author_role": "Chair",
        "published_on": date(2026, 1, 20),
        "read_minutes": 7,
        "tags": ["6G", "Nokia", "Wireless", "AI"],
    },
]


async def _seed_table(model: type[_M], rows: list[dict[str, Any]], session: AsyncSession) -> int:
    inserted = 0
    for row in rows:
        existing = await session.execute(select(model).where(model.slug == row["slug"]))
        if existing.scalar_one_or_none() is not None:
            continue
        session.add(model(**row))
        inserted += 1
    return inserted


async def main() -> None:
    async with SessionLocal() as session, session.begin():
        events_added = await _seed_table(Event, EVENTS, session)
        posts_added = await _seed_table(Post, POSTS, session)
    print(f"Seeded: events={events_added}, posts={posts_added} (skipped duplicates).")


if __name__ == "__main__":
    asyncio.run(main())
