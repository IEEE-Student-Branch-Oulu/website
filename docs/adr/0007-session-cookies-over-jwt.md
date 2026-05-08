# 0007 — Session cookies over JWT

- **Status:** Accepted
- **Date:** 2026-05-08
- **Deciders:** Ahmed Zuhayr (maintainer)

## Context

The backend serves a first-party Nuxt SPA on the same origin. We needed to choose between stateless JWTs (stored in localStorage or cookies) and server-side sessions with opaque tokens in HttpOnly cookies for authentication.

## Decision

Use server-side sessions keyed by an opaque 32-byte base64url token. The token is SHA-256 hashed before storage in the `sessions` table. The raw token is delivered as an `ieee_sid` HttpOnly, Secure, SameSite=Lax cookie with a 14-day idle timeout and 30-day absolute expiry.

## Consequences

- Positive: instant session revocation (suspend user, password change, logout-everywhere) — just mark rows as revoked.
- Positive: no localStorage means no XSS-accessible tokens.
- Positive: `last_seen_at` tracking comes for free on every authenticated request.
- Negative / accepted cost: requires a `sessions` table and a DB lookup per request (negligible at our scale).
- Follow-ups required: if we add a mobile app or cross-origin consumer, we may need to revisit or add an OAuth2 token flow alongside sessions.

## Alternatives considered

- **JWT in HttpOnly cookie** — still stateless, but revocation requires a blocklist (effectively a session table anyway). No real upside for a single-origin SPA.
- **JWT in localStorage** — standard SPA pattern, but exposes tokens to XSS. Refresh-token rotation adds complexity with no benefit here.
