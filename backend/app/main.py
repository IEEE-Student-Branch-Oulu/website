"""FastAPI application factory."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1 import api_router
from app.auth.csrf import CSRFMiddleware
from app.config import Settings, get_settings
from app.core.email import ConsoleBackend, MemoryBackend, ResendBackend, configure_backend
from app.core.errors import register_exception_handlers
from app.core.rate_limit import register_rate_limit_handler
from app.db import engine


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)

    app = FastAPI(
        title="IEEE SB Oulu API",
        version=__version__,
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _configure_email(settings)

    register_exception_handlers(app)
    register_rate_limit_handler(app)
    app.add_middleware(CSRFMiddleware)
    app.include_router(api_router)
    return app


def _configure_email(settings: Settings) -> None:
    log = logging.getLogger(__name__)
    if settings.email_backend == "resend":
        if not settings.email_resend_api_key:
            log.warning(
                "EMAIL_BACKEND=resend but EMAIL_RESEND_API_KEY is empty — falling back to console"
            )
            configure_backend(ConsoleBackend())
        else:
            configure_backend(ResendBackend(settings.email_resend_api_key, settings.email_from))
            log.info("Email backend: resend (from=%s)", settings.email_from)
    elif settings.email_backend == "memory":
        configure_backend(MemoryBackend())
        log.info("Email backend: memory (emails stored in memory)")
    else:
        configure_backend(ConsoleBackend())
        log.info("Email backend: console (emails print to stdout)")


app = create_app()
