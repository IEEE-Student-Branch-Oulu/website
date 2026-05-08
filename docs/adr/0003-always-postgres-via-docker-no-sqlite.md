# 0003 — Always Postgres via Docker (no SQLite shortcut)

- **Status:** Accepted
- **Date:** 2026-05-07
- **Deciders:** Backend foundation plan

## Context

A common pattern is to use SQLite for local development and Postgres in
production. It removes a dependency from the contributor's machine and
shaves a step off `make install`.

It also routinely costs hours of debugging when production breaks on a
JSONB query, a timezone, or a full-text search expression that worked
locally on SQLite. We use JSONB for `tags`, `DateTime(timezone=True)`,
and will likely use FTS later — exactly the surface that diverges.

## Decision

Local development always uses **Postgres 16 in Docker**. There is no
SQLite fallback. `docker compose up -d db` is part of `make dev`. Tests
also target Postgres (CI provides it via a service container; locally
the same dev DB or a `_test` URL works).

## Consequences

- Positive: dev and prod behave the same. JSONB queries, `now()`
  defaults, and timezone handling all match.
- Positive: fewer SQLAlchemy `with_variant(...)` workarounds in the
  models.
- Negative / accepted cost: contributors must have Docker installed.
  README documents this prominently and `make dev` fails fast with a
  clear error if Docker isn't running.
- Follow-up: revisit if we ever need to run the suite without Docker
  (e.g. on a managed CI without container support). Unlikely for a
  branch site.

## Alternatives considered

- **SQLite locally, Postgres in prod** — fast install, but parity bugs
  cost more than the install time saves.
- **Embedded Postgres (e.g. embedded-postgres-binaries)** — works on
  Linux/macOS, painful on Windows, and we'd still need Docker for
  multi-service compose.
