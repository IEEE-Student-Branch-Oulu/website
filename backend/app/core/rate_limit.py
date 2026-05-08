"""Rate limiting via slowapi.

In dev/test: in-memory storage. In prod with ``REDIS_URL``: Redis-backed.
When a limit is exceeded, slowapi raises ``RateLimitExceeded`` which our
handler converts to a 429 problem+json response.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.errors import PROBLEM_MEDIA_TYPE

limiter = Limiter(key_func=get_remote_address)

LOGIN_LIMIT = "5/minute"
REGISTER_LIMIT = "5/hour"
FORGOT_LIMIT = "3/hour"
RESEND_LIMIT = "3/hour"
RESET_LIMIT = "5/hour"


def register_rate_limit_handler(app: FastAPI) -> None:
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def _rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
        return JSONResponse(
            status_code=429,
            content={
                "type": "about:blank",
                "title": "Too Many Requests",
                "status": 429,
                "detail": f"Rate limit exceeded: {exc.detail}",
            },
            media_type=PROBLEM_MEDIA_TYPE,
        )
