"""Blog post ORM model.

We store the raw markdown source. `bodyHtml` and `headings[]` are
re-rendered on read by `service.render_full`. Trades a few ms of
render cost for editability and storage simplicity.
"""

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    body_md: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str] = mapped_column(String(40), nullable=False)

    author_name: Mapped[str] = mapped_column(String(120), nullable=False)
    author_initials: Mapped[str] = mapped_column(String(8), nullable=False)
    author_role: Mapped[str] = mapped_column(String(120), nullable=False)

    published_on: Mapped[date] = mapped_column(Date, nullable=False)
    read_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    tags: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
