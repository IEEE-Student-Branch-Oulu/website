"""Members endpoints: profile, directory, GDPR, renewal."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request, Response

from app.auth.dependencies import CurrentUser, RequireActive
from app.auth.models import AuditAction
from app.auth.service import renew_membership
from app.auth.sessions import delete_session_cookie, revoke_all_sessions
from app.config import get_settings
from app.core.audit import record
from app.core.pagination import Page
from app.deps import DBSession, PaginationDep
from app.domains.members.repository import list_directory
from app.domains.members.schemas import (
    MembershipPeriodRead,
    ProfileUpdate,
    UserPublic,
    UserSelf,
)
from app.domains.members.service import (
    gdpr_export,
    get_self_with_periods,
    soft_delete,
    update_profile,
)

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/me")
async def me_profile(user: CurrentUser, db: DBSession) -> UserSelf:
    return await get_self_with_periods(db, user)


@router.patch("/me")
async def update_me(
    request: Request,
    body: ProfileUpdate,
    user: RequireActive,
    db: DBSession,
) -> UserSelf:
    await update_profile(db, user, body)
    await record(
        db,
        action=AuditAction.profile_update,
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
    )
    await db.commit()
    return await get_self_with_periods(db, user)


@router.delete("/me", status_code=204)
async def delete_me(
    request: Request,
    user: CurrentUser,
    db: DBSession,
    response: Response,
) -> None:
    await soft_delete(db, user)
    await revoke_all_sessions(db, user.id)
    await record(
        db,
        action=AuditAction.gdpr_delete,
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
    )
    await db.commit()
    delete_session_cookie(response, secure=not get_settings().is_dev)


@router.get("/me/export")
async def export_me(
    request: Request,
    user: CurrentUser,
    db: DBSession,
) -> dict[str, Any]:
    data = await gdpr_export(db, user)
    await record(
        db,
        action=AuditAction.gdpr_export,
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
    )
    await db.commit()
    return data


@router.post("/me/renew", status_code=201)
async def renew_me(
    request: Request,
    user: CurrentUser,
    db: DBSession,
) -> MembershipPeriodRead:
    period = await renew_membership(db, user=user)
    await record(
        db,
        action=AuditAction.membership_renew,
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
        metadata={"period_year": period.period_year},
    )
    await db.commit()
    return MembershipPeriodRead.model_validate(period, from_attributes=True)


@router.get("/")
async def directory(
    db: DBSession,
    pagination: PaginationDep,
    _user: RequireActive,
) -> Page[UserPublic]:
    rows, total = await list_directory(db, limit=pagination.limit, offset=pagination.offset)
    return Page(
        items=[UserPublic.model_validate(u, from_attributes=True) for u in rows],
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )
