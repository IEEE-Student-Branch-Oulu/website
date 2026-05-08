"""initial schema: events, posts

Revision ID: 0001
Revises:
Create Date: 2026-05-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("location_url", sa.String(length=500), nullable=True),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("rsvp_link", sa.String(length=500), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column(
            "attendees_count", sa.Integer(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column("speaker_name", sa.String(length=120), nullable=True),
        sa.Column("speaker_title", sa.String(length=200), nullable=True),
        sa.Column(
            "is_highlighted", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column(
            "tags",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("slug", name="uq_events_slug"),
    )
    op.create_index("ix_events_slug", "events", ["slug"], unique=False)

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=False),
        sa.Column("excerpt", sa.Text(), nullable=False),
        sa.Column("body_md", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("author_name", sa.String(length=120), nullable=False),
        sa.Column("author_initials", sa.String(length=8), nullable=False),
        sa.Column("author_role", sa.String(length=120), nullable=False),
        sa.Column("published_on", sa.Date(), nullable=False),
        sa.Column("read_minutes", sa.Integer(), nullable=False),
        sa.Column(
            "tags",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "featured", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("slug", name="uq_posts_slug"),
    )
    op.create_index("ix_posts_slug", "posts", ["slug"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_posts_slug", table_name="posts")
    op.drop_table("posts")
    op.drop_index("ix_events_slug", table_name="events")
    op.drop_table("events")
