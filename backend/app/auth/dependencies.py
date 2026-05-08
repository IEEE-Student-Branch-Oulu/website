"""FastAPI dependencies for authentication and authorization."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from app.auth.sessions import COOKIE_NAME, load_session
from app.core.errors import AuthenticationError, PermissionDeniedError
from app.deps import DBSession
from app.domains.members.models import Role, User, UserStatus
from app.domains.members.repository import get_by_id


async def _get_current_user(request: Request, db: DBSession) -> User | None:
    raw_token = request.cookies.get(COOKIE_NAME)
    if not raw_token:
        return None

    session = await load_session(db, raw_token)
    if session is None:
        return None

    return await get_by_id(db, session.user_id)


async def _require_user(request: Request, db: DBSession) -> User:
    user = await _get_current_user(request, db)
    if user is None:
        raise AuthenticationError("Authentication required.")
    return user


async def _require_active(request: Request, db: DBSession) -> User:
    user = await _require_user(request, db)
    if user.status != UserStatus.active:
        raise PermissionDeniedError("Active membership required.")
    return user


async def _require_admin(request: Request, db: DBSession) -> User:
    user = await _require_active(request, db)
    if user.role != Role.admin:
        raise PermissionDeniedError("Admin access required.")
    return user


OptionalCurrentUser = Annotated[User | None, Depends(_get_current_user)]
CurrentUser = Annotated[User, Depends(_require_user)]
RequireActive = Annotated[User, Depends(_require_active)]
RequireAdmin = Annotated[User, Depends(_require_admin)]
