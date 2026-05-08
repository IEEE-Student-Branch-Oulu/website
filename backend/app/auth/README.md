# auth/ — Authentication and session management

This module handles user registration, login/logout, email verification, password management, and session lifecycle. It does **not** own the `User` model (that lives in `app/domains/members/`) — it owns the auth-specific tables (`Session`, `EmailToken`, `AuditLog`) and the request-handling logic around identity.

## Module layout

| File | Responsibility |
|---|---|
| `routers.py` | FastAPI endpoints: register, login, logout, me, verify-email, resend-verify, forgot-password, reset-password, change-password |
| `service.py` | Orchestration: register flow, login verification, token consumption, password changes, membership renewal |
| `dependencies.py` | FastAPI deps: `CurrentUser`, `OptionalCurrentUser`, `RequireActive`, `RequireAdmin` |
| `passwords.py` | Argon2id hashing, `needs_rehash` auto-upgrade, HIBP k-anonymity breach check |
| `tokens.py` | Opaque token generation (`secrets.token_urlsafe`), SHA-256 hashing |
| `sessions.py` | Session create/load/revoke, cookie set/delete helpers |
| `csrf.py` | Double-submit CSRF middleware |
| `models.py` | SQLAlchemy models: `Session`, `EmailToken`, `AuditLog`, enums |
| `schemas.py` | Pydantic request/response models for auth endpoints |

## Key design decisions

- **Server-side sessions** over JWT (ADR 0007) — instant revocation, no localStorage XSS risk.
- **Argon2id** with OWASP 2024 params (ADR 0008) — auto-rehash on login if params change.
- **HIBP breach check** — fail closed on confirmed breach, fail open on network error.
- **No user enumeration** — register returns 200 on duplicate, login uses constant-time dummy hash, forgot-password always returns 204.
- **Double-submit CSRF** — `ieee_csrf` non-HttpOnly cookie + `X-CSRF-Token` header on mutating requests.

## How to extend

**Adding a new auth endpoint:** add the route in `routers.py`, business logic in `service.py`. Use `CurrentUser`/`RequireActive`/`RequireAdmin` from `dependencies.py`.

**Adding a new email template:** create `{name}.html` and `{name}.txt` in `app/emails/templates/`, extending `_base.html`/`_base.txt`. Call `send(render("name", **ctx))` from the service layer.

**Adding 2FA (planned for v2):** add `totp_secret` and `totp_enabled` to `User`, a TOTP verification step in `login()`, an enrollment endpoint, and recovery codes. The session model already supports this — just gate session creation on TOTP verification.

**Adding OAuth (planned for v2):** add an `OAuthAccount` model linked to `User`, implement the authorization code flow via `authlib`, and create new routes in `routers.py`. Existing session infrastructure handles post-OAuth login.
