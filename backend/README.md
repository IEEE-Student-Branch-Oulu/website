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
make test           # pytest + coverage (≥60%)
make lint           # ruff check + mypy
make fmt            # ruff format
make migrate m="add X to events"   # autogenerate alembic migration
```

## CLI tools

```bash
# Promote a user to admin
uv run python -m app.scripts.manage_user promote user@example.com

# Activate a user (skip board approval)
uv run python -m app.scripts.manage_user activate user@example.com

# Seed demo data
uv run python -m scripts.seed
```

## Layout

```
app/
  main.py              # app factory, CORS, CSRF, rate limits, email backend
  config.py            # pydantic-settings (db, cors, auth, email, app)
  db.py                # async engine, session
  deps.py              # FastAPI dependencies (DB, pagination)
  api/v1/              # thin HTTP routers (events, posts, members, admin)
  domains/
    events/            # models, schemas, service, repository
    posts/
    members/           # User + MembershipPeriod models, profile, GDPR, directory
  core/                # pagination, errors, slug, markdown, email, audit, rate_limit
  auth/                # register, login, sessions, CSRF, passwords (argon2id), tokens
  emails/templates/    # Jinja2 HTML+text email templates
  scripts/             # promote_admin, seed
alembic/               # migrations (committed)
tests/                 # pytest + httpx AsyncClient
```

**Layering rule:** routers handle HTTP only → `service.py` holds logic → `repository.py` is the only place that touches the SQLAlchemy session. Keep new code consistent with this.

## Environment variables

See `.env.example` for the full list. Key additions for auth:

| Variable | Default | Description |
|---|---|---|
| `EMAIL_BACKEND` | `console` | `console`, `memory`, or `resend` |
| `EMAIL_FROM` | `IEEE SB Oulu <noreply@ieee-oulu.fi>` | Sender address |
| `RESEND_API_KEY` | — | Required when `EMAIL_BACKEND=resend` |
| `APP_PUBLIC_BASE_URL` | `http://localhost:3000` | Used in email links |

## Why these choices?

See the ADRs at [/docs/adr/](../docs/adr/). Highlights:

- [0001 — uv for Python dependencies](../docs/adr/0001-use-uv-for-python-dependencies.md)
- [0002 — SQLAlchemy 2.0 over SQLModel](../docs/adr/0002-sqlalchemy-2-over-sqlmodel.md)
- [0003 — Always Postgres via Docker](../docs/adr/0003-always-postgres-via-docker-no-sqlite.md)
- [0004 — RFC 7807 problem+json error format](../docs/adr/0004-rfc7807-problem-json-error-format.md)
- [0005 — Offset/limit pagination](../docs/adr/0005-offset-limit-pagination.md)
- [0006 — Monorepo layout](../docs/adr/0006-monorepo-frontend-backend-layout.md)
- [0007 — Session cookies over JWT](../docs/adr/0007-session-cookies-over-jwt.md)
- [0008 — Argon2id passwords](../docs/adr/0008-argon2id-passwords.md)
- [0009 — Resend email with pluggable backends](../docs/adr/0009-resend-email-with-pluggable-backends.md)
- [0010 — Single role RBAC](../docs/adr/0010-single-role-rbac.md)
- [0011 — GDPR soft delete and export](../docs/adr/0011-gdpr-soft-delete-and-export.md)
