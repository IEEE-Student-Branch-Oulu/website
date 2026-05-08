# 0011 — GDPR soft delete and data export

- **Status:** Accepted
- **Date:** 2026-05-08
- **Deciders:** Ahmed Zuhayr (maintainer)

## Context

The site stores personal data of EU-based university students (names, emails, IEEE membership numbers). GDPR requires the right to data portability (Article 20) and the right to erasure (Article 17). We needed to decide how deletion works given that audit logs reference user IDs.

## Decision

Implement soft delete with anonymization. When a user deletes their account:

1. `deleted_at` is set to the current timestamp.
2. Personal fields (email, first/last name, bio, consents) are overwritten with anonymized placeholders.
3. All sessions are revoked.
4. The user row remains for referential integrity (audit log FKs use `SET NULL`).

Data export returns a JSON file containing all user-owned data (profile, membership periods, consent records) with a generation timestamp.

## Consequences

- Positive: complies with GDPR erasure — personal data is destroyed, not just hidden.
- Positive: audit log integrity is preserved (actor/target FKs become NULL, but the log entry itself remains).
- Positive: export is self-service — no admin intervention needed.
- Negative / accepted cost: soft-deleted rows accumulate. At our scale this is negligible; add a cleanup job if it ever matters.
- Follow-ups required: review anonymization completeness if new personal fields are added to the User model.

## Alternatives considered

- **Hard delete with CASCADE** — destroys audit trail. Unacceptable for accountability.
- **Hard delete with archive table** — more complex, same result. Soft delete is simpler and standard.
