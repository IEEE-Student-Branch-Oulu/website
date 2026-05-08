"""Double-submit CSRF protection.

Sets a non-HttpOnly ``ieee_csrf`` cookie on every response. Mutating
requests must echo the value in the ``X-CSRF-Token`` header.  Safe
methods (GET, HEAD, OPTIONS) and unauthenticated requests are exempt.
"""

from __future__ import annotations

import secrets

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.auth.sessions import COOKIE_NAME as SESSION_COOKIE
from app.core.errors import DomainError, _problem

CSRF_COOKIE = "ieee_csrf"
CSRF_HEADER = "X-CSRF-Token"
SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


class CSRFError(DomainError):
    status_code = 403
    title = "CSRF Validation Failed"


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        csrf_cookie = request.cookies.get(CSRF_COOKIE)

        if request.method not in SAFE_METHODS and request.cookies.get(SESSION_COOKIE):
            header_val = request.headers.get(CSRF_HEADER)
            if (
                not csrf_cookie
                or not header_val
                or not secrets.compare_digest(csrf_cookie, header_val)
            ):
                return _problem(
                    status=403,
                    title="CSRF Validation Failed",
                    detail="Missing or mismatched CSRF token.",
                )

        response = await call_next(request)

        if not csrf_cookie:
            token = secrets.token_urlsafe(32)
            response.set_cookie(
                key=CSRF_COOKIE,
                value=token,
                httponly=False,
                secure=request.url.scheme == "https",
                samesite="lax",
                path="/",
            )

        return response
