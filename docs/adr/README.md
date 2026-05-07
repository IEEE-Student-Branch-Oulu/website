# Architecture Decision Records

This directory captures the **why** behind major technical choices in the
project. Each ADR is a short, dated record of a single decision: the
problem we faced, the option we picked, and the consequences we accepted.

ADRs exist so future board members can answer "why did we pick X?" without
having to dig through chat history or commit messages.

## When to write one

Write an ADR when you're making a decision that:

- Will be hard or expensive to reverse (DB engine, language, framework).
- Affects how contributors work day-to-day (tooling, layout, conventions).
- Picks one of several reasonable options where the tradeoffs aren't obvious.

You do **not** need an ADR for routine implementation choices, bug fixes,
or things already documented well in code.

## How to write one

1. Copy [`template.md`](./template.md) to a new file. Use the next number in
   sequence and a short kebab-case slug:
   `0007-pick-something-meaningful.md`.
2. Fill in **Context**, **Decision**, **Consequences**, and **Alternatives
   considered**. Keep it short — half a page to one page. Reviewers should be
   able to scan it.
3. Set `Status: Accepted` and open a PR. Discuss in the PR; merge when there
   is consensus.

## Append-only

ADRs are **never edited after merge**. If a decision is reversed, write a
new ADR with `Status: Supersedes 0003` (or similar) and a reference to the
prior one. The old ADR stays in place as historical context. This keeps the
record honest about what we knew when.

## Index

| #    | Title                                                  | Status |
|------|--------------------------------------------------------|--------|
| 0001 | [Use uv for Python dependencies](./0001-use-uv-for-python-dependencies.md) | Accepted |
| 0002 | [SQLAlchemy 2.0 over SQLModel](./0002-sqlalchemy-2-over-sqlmodel.md) | Accepted |
| 0003 | [Always Postgres via Docker (no SQLite shortcut)](./0003-always-postgres-via-docker-no-sqlite.md) | Accepted |
| 0004 | [RFC 7807 problem+json error format](./0004-rfc7807-problem-json-error-format.md) | Accepted |
| 0005 | [Offset/limit pagination](./0005-offset-limit-pagination.md) | Accepted |
| 0006 | [Monorepo frontend/backend layout](./0006-monorepo-frontend-backend-layout.md) | Accepted |
