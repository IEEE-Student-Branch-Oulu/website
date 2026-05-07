"""v1 API router. New domain routers register themselves here."""

from fastapi import APIRouter

from app.api.v1 import events, health, posts

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(events.router)
api_router.include_router(posts.router)
