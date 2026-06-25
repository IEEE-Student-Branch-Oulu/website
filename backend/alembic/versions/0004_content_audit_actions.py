"""content audit actions

Adds content_create / content_update / content_delete values to the
audit_action enum so post/event mutations can be recorded.

Revision ID: 0004
Revises: 0003
Create Date: 2026-06-25
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_NEW_VALUES = ("content_create", "content_update", "content_delete")


def upgrade() -> None:
    # ADD VALUE IF NOT EXISTS is idempotent and (PG12+) safe inside the
    # migration transaction since the new values aren't used here.
    for value in _NEW_VALUES:
        op.execute(f"ALTER TYPE audit_action ADD VALUE IF NOT EXISTS '{value}'")


def downgrade() -> None:
    # PostgreSQL cannot drop enum values; leaving them is harmless.
    pass
