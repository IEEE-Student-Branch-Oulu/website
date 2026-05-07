#!/usr/bin/env bash
# Fallback for systems without `make`. Prefer `make dev`.
set -euo pipefail

cd "$(dirname "$0")/.."

uv sync
docker compose up -d db
echo "waiting for postgres..."
until docker compose exec -T db pg_isready -U ieee >/dev/null 2>&1; do sleep 0.5; done
uv run alembic upgrade head
exec uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
