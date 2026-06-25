"""cms image + recap link fields

Adds cover_image_url to posts and events, plus an optional event_slug
link on posts (an event-recap post pointing back to its past event).

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("cover_image_url", sa.String(length=500), nullable=True))
    op.add_column("posts", sa.Column("event_slug", sa.String(length=200), nullable=True))
    op.add_column("events", sa.Column("cover_image_url", sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column("events", "cover_image_url")
    op.drop_column("posts", "event_slug")
    op.drop_column("posts", "cover_image_url")
