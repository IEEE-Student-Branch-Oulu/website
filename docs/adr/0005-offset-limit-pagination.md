# 0005 — Offset/limit pagination

- **Status:** Accepted
- **Date:** 2026-05-07
- **Deciders:** Backend foundation plan

## Context

List endpoints (`/events`, `/posts`) need pagination. The two main shapes
are offset/limit and cursor-based. Cursor is more correct under heavy
write load (no skipped/duplicated items as new rows arrive) but is
harder to integrate with frontend table/list components and harder to
debug.

The dataset here is **branch-scale**: hundreds to low thousands of rows
across the lifetime of the site. Concurrent writes are rare. The
frontend wants page numbers and total counts to render pagers.

## Decision

Use **offset/limit** pagination. The list-response envelope is:

```json
{ "items": [...], "total": 42, "limit": 20, "offset": 0 }
```

`limit` is bounded to `[1, 100]`. The `Page[T]` envelope lives in
`app/core/pagination.py` and is reused across domains.

## Consequences

- Positive: trivial to render a pager on the frontend; `total` lets us
  show "page 3 of 7."
- Positive: easy to debug (just a SQL `LIMIT/OFFSET`).
- Negative / accepted cost: deep pagination scans skipped rows. At
  branch-scale this is irrelevant; if a domain ever needs cursor
  pagination it can opt into a different envelope.
- Follow-up: revisit if we ever ship a feed-style endpoint with
  thousands of items per query.

## Alternatives considered

- **Cursor (keyset) pagination** — correct under writes but more code,
  harder UX, no `total` without an extra query. Overkill here.
- **Page-number** — same as offset/limit with worse arithmetic.
