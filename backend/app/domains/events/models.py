"""SQLAlchemy ORM model for events.

`status` and `spots_left` are NOT stored — they are derived in
`service.py` from the date and `attendees_count` so the database holds
only the source-of-truth fields.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # Stored UTC; service layer formats display strings in branch timezone.
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    location: Mapped[str] = mapped_column(String(200), nullable=False)
    location_url: Mapped[str | None] = mapped_column(String(500))

    type: Mapped[str] = mapped_column(String(20), nullable=False)
    rsvp_link: Mapped[str | None] = mapped_column(String(500))
    capacity: Mapped[int | None] = mapped_column(Integer)
    attendees_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    speaker_name: Mapped[str | None] = mapped_column(String(120))
    speaker_title: Mapped[str | None] = mapped_column(String(200))
    is_highlighted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    tags: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
