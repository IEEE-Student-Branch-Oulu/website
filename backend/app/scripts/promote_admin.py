"""Backwards-compatible wrapper — use manage_user instead.

Usage: uv run python -m app.scripts.promote_admin user@example.com
"""

from __future__ import annotations

import asyncio
import sys

from app.scripts.manage_user import promote


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: uv run python -m app.scripts.promote_admin <email>")
        sys.exit(1)
    asyncio.run(promote(sys.argv[1]))


if __name__ == "__main__":
    main()
