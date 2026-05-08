"""v1 API router. New domain routers register themselves here."""

from fastapi import APIRouter

from app.api.v1 import admin, events, health, posts
from app.auth.routers import router as auth_router
from app.domains.members.routers import router as members_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(events.router)
api_router.include_router(posts.router)
api_router.include_router(auth_router)
api_router.include_router(members_router)
api_router.include_router(admin.router)
