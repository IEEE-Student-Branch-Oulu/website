"""RFC 7807 problem+json error responses.

One global handler converts FastAPI / Starlette HTTPException and our own
domain exceptions into a uniform `application/problem+json` body so the
frontend can write a single error renderer.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status as _status
from starlette.exceptions import HTTPException as StarletteHTTPException

PROBLEM_MEDIA_TYPE = "application/problem+json"


class DomainError(Exception):
    """Base class for application-defined errors that map to HTTP responses."""

    status_code: int = _status.HTTP_500_INTERNAL_SERVER_ERROR
    title: str = "Internal Server Error"

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(detail or self.title)
        self.detail = detail or self.title


class NotFoundError(DomainError):
    status_code = _status.HTTP_404_NOT_FOUND
    title = "Not Found"


def _problem(
    *, status: int, title: str, detail: str, type_: str = "about:blank", **extra: Any
) -> JSONResponse:
    body: dict[str, Any] = {"type": type_, "title": title, "status": status, "detail": detail}
    body.update(extra)
    return JSONResponse(content=body, status_code=status, media_type=PROBLEM_MEDIA_TYPE)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain_handler(_request: Request, exc: DomainError) -> JSONResponse:
        return _problem(status=exc.status_code, title=exc.title, detail=exc.detail)

    @app.exception_handler(StarletteHTTPException)
    async def _http_handler(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return _problem(
            status=exc.status_code,
            title=_status_title(exc.status_code),
            detail=str(exc.detail) if exc.detail else _status_title(exc.status_code),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
        return _problem(
            status=422,
            title="Unprocessable Entity",
            detail="Request validation failed.",
            errors=exc.errors(),
        )


def _status_title(code: int) -> str:
    return {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        409: "Conflict",
        422: "Unprocessable Entity",
        500: "Internal Server Error",
    }.get(code, "Error")


# Re-exported for unit tests
__all__ = [
    "PROBLEM_MEDIA_TYPE",
    "DomainError",
    "NotFoundError",
    "register_exception_handlers",
]


_HandlerT = Callable[[Request, Exception], Awaitable[JSONResponse]]
"""Internal alias kept for documentation; not used at runtime."""
