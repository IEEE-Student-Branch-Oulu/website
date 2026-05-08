# Security

## Reporting vulnerabilities

If you discover a security vulnerability, please report it responsibly via email to **ahmed.zuhayr@student.oulu.fi**. Do not open a public issue.

We aim to acknowledge reports within 48 hours and provide a fix or mitigation plan within 7 days.

## Threat model

The primary threats we design against:

### Account takeover

- **Mitigation:** argon2id password hashing (ADR 0008), HIBP breach check on registration and password change, 12-character minimum, rate-limited login (5/min/IP, 10/hour/email).
- **Session security:** opaque tokens hashed with SHA-256 at rest, HttpOnly Secure SameSite=Lax cookies, 14-day idle / 30-day absolute expiry.
- **Password reset:** single-use tokens with 1-hour expiry, all sessions revoked on password change.

### User enumeration

- **Registration:** returns 200 even if email exists (no new row created).
- **Login:** constant-time comparison against a dummy hash for unknown emails, generic error message for all failure modes.
- **Forgot password:** always returns 204 regardless of whether the email exists.

### Cross-Site Request Forgery (CSRF)

- **Mitigation:** double-submit pattern. A non-HttpOnly `ieee_csrf` cookie is set on every response; mutating requests must include a matching `X-CSRF-Token` header. SameSite=Lax provides defence-in-depth.

### Cross-Site Scripting (XSS)

- **Mitigation:** session tokens are in HttpOnly cookies (inaccessible to JavaScript). Vue's template system auto-escapes output. No `v-html` with user content.

### Insecure Direct Object References (IDOR)

- **Mitigation:** member endpoints operate on `current_user` (derived from session), not URL parameters. Admin endpoints require the `RequireAdmin` dependency. Directory listings respect `profile_visibility`.

### Privilege escalation

- **Mitigation:** single role enum checked via `RequireAdmin` dependency on every admin endpoint. Last-admin guard prevents demoting the final admin, avoiding lockout.

## Session lifecycle

| Event | Action |
|---|---|
| Login | New session created, cookie set |
| Logout | Session revoked, cookie deleted |
| Password change | All other sessions revoked |
| Password reset | All sessions revoked |
| Admin suspends user | All sessions revoked |
| Admin demotes user | All sessions revoked |
| Account deletion | All sessions revoked, cookie deleted |

## Rate limits

| Endpoint | Limit |
|---|---|
| Login | 5/minute/IP |
| Register | 5/hour/IP |
| Forgot password | 3/hour/email |
| Resend verification | 3/hour/email |
| Password reset | 5/hour/IP |

Rate limit responses use RFC 7807 problem+json with status 429.

## Data protection

See ADR 0011 for GDPR compliance details. Personal data is anonymized on account deletion. Data export is available as self-service JSON download.
