# 0009 — Resend email with pluggable backends

- **Status:** Accepted
- **Date:** 2026-05-08
- **Deciders:** Ahmed Zuhayr (maintainer)

## Context

The auth system sends transactional emails (verification, password reset, admin notifications). We need a sending mechanism that works in production, development, and tests without requiring external API keys for local work.

## Decision

Use Resend as the production email provider, wrapped behind a pluggable `EmailBackend` protocol with three implementations:

- **ConsoleBackend** (default in dev): logs email content to stdout.
- **MemoryBackend** (tests): stores sent messages in a list for assertions.
- **ResendBackend** (prod): sends via Resend's HTTP API using httpx.

Templates are Jinja2 HTML+text pairs in `app/emails/templates/`, rendered at send time. The backend is selected by the `EMAIL_BACKEND` env var.

## Consequences

- Positive: new contributors can run the full registration flow without a Resend key.
- Positive: tests assert on actual email content without mocking or network calls.
- Positive: swapping providers (e.g., to SES or Postmark) means writing one new class.
- Negative / accepted cost: Jinja2 templates are an extra dependency, though it's lightweight and already common in Python.
- Follow-ups required: add HTML email previews to the dev workflow if template count grows.

## Alternatives considered

- **SendGrid / SES** — heavier SDKs, more config. Resend has a simpler API and generous free tier.
- **smtp via aiosmtplib** — requires an SMTP server in dev; adds infrastructure complexity for no benefit at our volume.
