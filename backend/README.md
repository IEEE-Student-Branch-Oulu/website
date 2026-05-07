# IEEE SB Oulu — Backend

FastAPI + PostgreSQL service powering the website.

## Quick start

You need Docker (for Postgres), Python 3.11+, and [`uv`](https://docs.astral.sh/uv/).

```bash
cd backend
cp .env.example .env
make install        # uv sync + pre-commit install
make dev            # postgres up, run migrations, launch uvicorn --reload
make seed           # in another terminal, once
```

Server runs at **http://localhost:8000** with interactive docs at **/docs**.

## Daily commands

```bash
make test           # pytest + coverage (≥70%)
make lint           # ruff check + mypy
make fmt            # ruff format
make migrate m="add X to events"   # autogenerate alembic migration
```

## Layout

```
app/
  main.py              # app factory, CORS, error handlers, router include
  config.py            # pydantic-settings (db, cors, auth-stub)
  db.py                # async engine, session
  deps.py              # FastAPI dependencies (DB, pagination)
  api/v1/              # thin HTTP routers
  domains/
    events/            # models, schemas, service, repository
    posts/
  core/                # pagination, errors, slug, markdown
  auth/                # placeholder — auth lands in a follow-up plan
alembic/               # migrations (committed)
scripts/seed.py        # idempotent demo data
tests/                 # pytest + httpx AsyncClient
```

**Layering rule:** routers handle HTTP only → `service.py` holds logic → `repository.py` is the only place that touches the SQLAlchemy session. Keep new code consistent with this.

## Why these choices?

See the ADRs at [/docs/adr/](../docs/adr/). Highlights:

- [0001 — uv for Python dependencies](../docs/adr/0001-use-uv-for-python-dependencies.md)
- [0002 — SQLAlchemy 2.0 over SQLModel](../docs/adr/0002-sqlalchemy-2-over-sqlmodel.md)
- [0003 — Always Postgres via Docker](../docs/adr/0003-always-postgres-via-docker-no-sqlite.md)
- [0004 — RFC 7807 problem+json error format](../docs/adr/0004-rfc7807-problem-json-error-format.md)
- [0005 — Offset/limit pagination](../docs/adr/0005-offset-limit-pagination.md)
- [0006 — Monorepo layout](../docs/adr/0006-monorepo-frontend-backend-layout.md)
