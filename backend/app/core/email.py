"""Pluggable email backends + Jinja2 template rendering.

Backends:
- ``ConsoleBackend`` — logs email to stdout (default in dev).
- ``MemoryBackend`` — stores emails in a list (for tests).
- ``ResendBackend`` — sends via the official Resend SDK (prod).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

from jinja2 import Environment, PackageLoader, select_autoescape

log = logging.getLogger(__name__)

_jinja_env = Environment(
    loader=PackageLoader("app", "emails/templates"),
    autoescape=select_autoescape(["html"]),
)


@dataclass
class EmailMessage:
    to: str
    subject: str
    html: str
    text: str


def render(template_name: str, **ctx: object) -> tuple[str, str]:
    """Return ``(html, text)`` for a template pair."""
    html = _jinja_env.get_template(f"{template_name}.html").render(**ctx)
    text = _jinja_env.get_template(f"{template_name}.txt").render(**ctx)
    return html, text


class EmailBackend(Protocol):
    async def send(self, message: EmailMessage) -> None: ...


class ConsoleBackend:
    """Prints email to stdout — no external service needed."""

    async def send(self, message: EmailMessage) -> None:
        print(
            f"\n{'=' * 60}\n"
            f"EMAIL TO: {message.to}\n"
            f"SUBJECT:  {message.subject}\n"
            f"{'─' * 60}\n"
            f"{message.text}\n"
            f"{'=' * 60}\n"
        )


class MemoryBackend:
    """Stores sent emails in memory — use in tests."""

    def __init__(self) -> None:
        self.outbox: list[EmailMessage] = []

    async def send(self, message: EmailMessage) -> None:
        self.outbox.append(message)


class ResendBackend:
    """Sends email via the official Resend SDK."""

    def __init__(self, api_key: str, from_address: str) -> None:
        self._from = from_address
        import resend

        resend.api_key = api_key

    async def send(self, message: EmailMessage) -> None:
        import resend

        params: resend.Emails.SendParams = {
            "from": self._from,
            "to": [message.to],
            "subject": message.subject,
            "html": message.html,
            "text": message.text,
        }
        try:
            result = resend.Emails.send(params)
            log.info("Resend email sent to %s (id=%s)", message.to, result.get("id"))
        except Exception:
            log.exception("Failed to send email via Resend to %s", message.to)
            raise


_backend: EmailBackend = ConsoleBackend()


def configure_backend(backend: EmailBackend) -> None:
    global _backend
    _backend = backend


def get_backend() -> EmailBackend:
    return _backend
