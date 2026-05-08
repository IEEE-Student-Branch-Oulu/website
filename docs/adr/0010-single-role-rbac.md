# 0010 — Single role RBAC (member / admin)

- **Status:** Accepted
- **Date:** 2026-05-08
- **Deciders:** Ahmed Zuhayr (maintainer)

## Context

The site needs role-based access control for admin functions (user approval, role changes, audit log). The branch has ~20-50 active members and a small board. We needed to decide between a simple role enum and a full permissions system.

## Decision

Use a single `Role` enum with two values: `member` and `admin`. Role is stored directly on the `User` model. Admin status is checked via a `RequireAdmin` FastAPI dependency. A last-admin guard prevents demoting the final admin.

## Consequences

- Positive: trivially simple to understand, implement, and audit.
- Positive: no join tables, no permission matrices, no role hierarchy logic.
- Positive: the last-admin guard prevents lockout — the most common footgun with simple RBAC.
- Negative / accepted cost: no granularity — you can't give someone "can edit events" without full admin. Acceptable for a small student branch.
- Follow-ups required: if the branch grows or needs roles like `editor` or `treasurer`, migrate to a many-to-many `user_roles` table. The single-enum design makes this migration straightforward.

## Alternatives considered

- **Many-to-many user/role/permission** — overkill for 2 roles and <50 users. Adds join tables, cache invalidation, and UI complexity.
- **Casbin / OPA** — policy engines designed for complex authorization. Massive overhead for our use case.
