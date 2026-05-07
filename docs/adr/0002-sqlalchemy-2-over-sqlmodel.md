# 0002 — SQLAlchemy 2.0 (async) over SQLModel

- **Status:** Accepted
- **Date:** 2026-05-07
- **Deciders:** Backend foundation plan

## Context

We need an ORM with first-class async support, type checking, and a
migration story (Alembic). SQLModel and SQLAlchemy 2.0's typed style are
the obvious candidates. SQLModel is friendlier on day 1 — one class
instead of two. SQLAlchemy is more verbose but is what the broader
ecosystem (Stack Overflow, blog posts, books) targets.

The decisive question for this project: **what happens at month 6?**
That's when the original author has rotated off the board and a new
student needs to add a relationship, write a migration, or debug a
nullable column that mysteriously isn't.

## Decision

Use **SQLAlchemy 2.0 async with Alembic** for migrations. Keep ORM
models and Pydantic schemas as separate types. Pydantic v2 with
`from_attributes=True` handles the mapping at API boundaries.

## Consequences

- Positive: every Stack Overflow answer about SQLAlchemy applies here.
  The typed `Mapped[]` style is now ergonomic.
- Positive: clean separation between persistence (`models.py`) and
  transport (`schemas.py`). Frontend-shaped fields stay in schemas.
- Negative / accepted cost: more upfront concepts (Mapped, mapped_column,
  Declarative Base) than SQLModel's "one class for everything." Worth it.
- Follow-up: keep the layering rule documented in `backend/README.md` so
  contributors don't accidentally let ORM models leak into routers.

## Alternatives considered

- **SQLModel** — friendlier first impression, but breaks down at
  Alembic autogeneration with relationships, optional fields, and
  custom types. Exactly the situations rotating maintainers hit.
- **Tortoise ORM, Piccolo, Edgy** — smaller communities, less material
  to read when something goes wrong.
