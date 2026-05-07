# 0004 — RFC 7807 `application/problem+json` for errors

- **Status:** Accepted
- **Date:** 2026-05-07
- **Deciders:** Backend foundation plan

## Context

FastAPI's default error response is `{"detail": "..."}`. That's fine for
small APIs but means the frontend writes one error renderer per shape
(404 vs 422 vs domain errors). We'd rather write that renderer once.

[RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) describes a
small, stable JSON shape for HTTP error responses:

```json
{ "type": "...", "title": "...", "status": 404, "detail": "..." }
```

It's used by enough public APIs (Spring, ASP.NET, several cloud providers)
that the convention is well understood.

## Decision

All error responses returned by the API use the
**`application/problem+json`** media type with the RFC 7807 shape. A
single global exception handler in `app/core/errors.py` converts
FastAPI/Starlette `HTTPException`, `RequestValidationError`, and our own
`DomainError` subclasses into this format.

## Consequences

- Positive: the frontend writes one error mapper. Adding a new domain
  error means subclassing `DomainError` and raising — no router-level
  try/except.
- Positive: validation errors include the FastAPI `errors` array under
  the `errors` key, preserving field-level detail for forms.
- Negative / accepted cost: ~30 lines of handler glue. The OpenAPI
  schema for error responses is slightly more work to keep aligned.
- Follow-up: add a `type` URI per error class once the documentation
  site exists (e.g. `https://ieee-oulu.fi/errors/event-not-found`).

## Alternatives considered

- **FastAPI default `{"detail": ...}`** — fine for tiny APIs, weak for a
  growing one. Frontend ends up branching on `typeof detail`.
- **JSON:API errors object** — more structure than we need; designed for
  multi-resource responses we don't have.
- **Custom shape** — every project that does this regrets it later.
