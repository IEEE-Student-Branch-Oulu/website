# 0008 — Argon2id for password hashing

- **Status:** Accepted
- **Date:** 2026-05-08
- **Deciders:** Ahmed Zuhayr (maintainer)

## Context

We need a password hashing algorithm for member accounts. The choice affects security against offline brute-force attacks and operational cost (CPU/memory per login).

## Decision

Use argon2id via `argon2-cffi` with OWASP 2024 baseline parameters: `time_cost=3`, `memory_cost=64 MiB`, `parallelism=4`. On login, `needs_rehash()` is checked so parameters auto-upgrade without forcing password resets.

Passwords must be at least 12 characters and pass a HIBP k-anonymity breach check (fail closed on confirmed match, fail open on network error).

## Consequences

- Positive: argon2id is the current OWASP recommendation — memory-hard, resistant to GPU/ASIC attacks.
- Positive: `needs_rehash` means we can tighten parameters later with zero user friction.
- Positive: HIBP check blocks the most commonly breached passwords with minimal UX cost.
- Negative / accepted cost: 64 MiB per hash limits concurrent logins on memory-constrained hosts (~100 concurrent at 6.4 GB). Fine for a student branch site.
- Follow-ups required: monitor OWASP recommendations and bump parameters periodically.

## Alternatives considered

- **bcrypt (via passlib)** — battle-tested but not memory-hard; OWASP now recommends argon2id over bcrypt for new projects.
- **scrypt** — memory-hard but less tunable and less ecosystem support in Python than argon2-cffi.
