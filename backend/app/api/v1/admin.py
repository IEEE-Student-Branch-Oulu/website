"""Admin endpoints: user management, membership approval, role changes, audit log, CSV export."""

from __future__ import annotations

import csv
import io
from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, File, Request, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import RequireAdmin
from app.auth.models import AuditAction, AuditLog
from app.auth.sessions import revoke_all_sessions
from app.config import get_settings
from app.core import storage
from app.core.audit import record
from app.core.email import EmailMessage, get_backend, render
from app.core.errors import ConflictError, NotFoundError
from app.core.pagination import Page
from app.deps import DBSession, PaginationDep
from app.domains.members.models import (
    MembershipPeriod,
    MembershipStatus,
    Role,
    User,
    UserStatus,
)
from app.domains.members.repository import (
    count_active_admins,
    get_by_id,
    list_paged,
    list_pending_approval,
    list_pending_renewals,
)
from app.domains.members.schemas import (
    MembershipPeriodRead,
    UserAdmin,
)

router = APIRouter(prefix="/admin", tags=["admin"])


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class RoleChangeRequest(_CamelModel):
    role: Role


class RejectRequest(_CamelModel):
    reason: str | None = None


class UploadResponse(_CamelModel):
    url: str


class AuditEntry(_CamelModel):
    id: int
    actor_user_id: int | None
    action: AuditAction
    target_user_id: int | None
    metadata: dict[str, Any]
    ip: str | None
    created_at: datetime


def _user_admin(user: User) -> UserAdmin:
    return UserAdmin.model_validate(user, from_attributes=True)


async def _get_target(db: AsyncSession, user_id: int) -> User:
    user = await get_by_id(db, user_id, include_deleted=True)
    if user is None:
        raise NotFoundError("User not found.")
    return user


@router.get("/users")
async def list_users(
    pagination: PaginationDep,
    db: DBSession,
    _admin: RequireAdmin,
    status: UserStatus | None = None,
    role: Role | None = None,
    q: str | None = None,
) -> Page[UserAdmin]:
    rows, total = await list_paged(
        db,
        limit=pagination.limit,
        offset=pagination.offset,
        status=status,
        role=role,
        q=q,
        include_deleted=False,
    )
    return Page(
        items=[_user_admin(u) for u in rows],
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/users/pending")
async def list_pending(
    pagination: PaginationDep,
    db: DBSession,
    _admin: RequireAdmin,
) -> Page[UserAdmin]:
    rows, total = await list_pending_approval(db, limit=pagination.limit, offset=pagination.offset)
    return Page(
        items=[_user_admin(u) for u in rows],
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/renewals/pending")
async def list_pending_renewals_endpoint(
    pagination: PaginationDep,
    db: DBSession,
    _admin: RequireAdmin,
    year: int | None = None,
) -> Page[MembershipPeriodRead]:
    from app.auth.service import _current_period_year

    y = year or _current_period_year()
    rows, total = await list_pending_renewals(
        db,
        year=y,
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return Page(
        items=[MembershipPeriodRead.model_validate(p, from_attributes=True) for p in rows],
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.post("/users/{user_id}/approve")
async def approve_user(
    user_id: int,
    request: Request,
    db: DBSession,
    admin: RequireAdmin,
) -> UserAdmin:
    target = await _get_target(db, user_id)
    if target.status != UserStatus.pending_approval:
        raise ConflictError("User is not pending approval.")

    target.status = UserStatus.active

    period = (
        await db.execute(
            select(MembershipPeriod)
            .where(
                MembershipPeriod.user_id == target.id,
            )
            .order_by(MembershipPeriod.period_year.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    if period and period.status == MembershipStatus.pending:
        period.status = MembershipStatus.approved
        period.reviewed_at = datetime.now(tz=UTC)
        period.reviewed_by = admin.id

    await record(
        db,
        action=AuditAction.approve,
        actor_user_id=admin.id,
        target_user_id=target.id,
        request=request,
    )
    await db.commit()

    settings = get_settings()
    html, text = render(
        "application_approved",
        first_name=target.first_name,
        period_year=period.period_year if period else 0,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=target.email,
            subject="Application approved - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )

    return _user_admin(target)


@router.post("/users/{user_id}/reject")
async def reject_user(
    user_id: int,
    request: Request,
    body: RejectRequest,
    db: DBSession,
    admin: RequireAdmin,
) -> UserAdmin:
    target = await _get_target(db, user_id)
    if target.status != UserStatus.pending_approval:
        raise ConflictError("User is not pending approval.")

    target.status = UserStatus.rejected

    period = (
        await db.execute(
            select(MembershipPeriod)
            .where(
                MembershipPeriod.user_id == target.id,
            )
            .order_by(MembershipPeriod.period_year.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    if period and period.status == MembershipStatus.pending:
        period.status = MembershipStatus.rejected
        period.reviewed_at = datetime.now(tz=UTC)
        period.reviewed_by = admin.id
        period.rejection_reason = body.reason

    await record(
        db,
        action=AuditAction.reject,
        actor_user_id=admin.id,
        target_user_id=target.id,
        metadata={"reason": body.reason},
        request=request,
    )
    await db.commit()

    settings = get_settings()
    html, text = render(
        "application_rejected",
        first_name=target.first_name,
        period_year=period.period_year if period else 0,
        reason=body.reason,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=target.email,
            subject="Application update - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )

    return _user_admin(target)


@router.post("/users/{user_id}/role")
async def change_role(
    user_id: int,
    request: Request,
    body: RoleChangeRequest,
    db: DBSession,
    admin: RequireAdmin,
) -> UserAdmin:
    target = await _get_target(db, user_id)

    if target.role == Role.admin and body.role == Role.member and target.id == admin.id:
        count = await count_active_admins(db)
        if count <= 1:
            raise ConflictError("Cannot remove the last admin.")

    old_role = target.role
    target.role = body.role

    await record(
        db,
        action=AuditAction.role_change,
        actor_user_id=admin.id,
        target_user_id=target.id,
        metadata={"old_role": old_role.value, "new_role": body.role.value},
        request=request,
    )

    if old_role == Role.admin and body.role == Role.member:
        await revoke_all_sessions(db, target.id)

    await db.commit()

    settings = get_settings()
    html, text = render(
        "role_changed",
        first_name=target.first_name,
        new_role=body.role.value,
        base_url=settings.public_base_url,
    )
    await get_backend().send(
        EmailMessage(
            to=target.email,
            subject="Role updated - IEEE SB Oulu",
            html=html,
            text=text,
        )
    )

    return _user_admin(target)


@router.post("/users/{user_id}/suspend")
async def suspend_user(
    user_id: int,
    request: Request,
    db: DBSession,
    admin: RequireAdmin,
) -> UserAdmin:
    target = await _get_target(db, user_id)
    if target.id == admin.id:
        raise ConflictError("Cannot suspend yourself.")

    target.status = UserStatus.suspended
    await revoke_all_sessions(db, target.id)

    await record(
        db,
        action=AuditAction.suspend,
        actor_user_id=admin.id,
        target_user_id=target.id,
        request=request,
    )
    await db.commit()
    return _user_admin(target)


@router.post("/users/{user_id}/restore")
async def restore_user(
    user_id: int,
    request: Request,
    db: DBSession,
    admin: RequireAdmin,
) -> UserAdmin:
    target = await _get_target(db, user_id)
    if target.status != UserStatus.suspended:
        raise ConflictError("User is not suspended.")

    target.status = UserStatus.active

    await record(
        db,
        action=AuditAction.restore,
        actor_user_id=admin.id,
        target_user_id=target.id,
        request=request,
    )
    await db.commit()
    return _user_admin(target)


@router.get("/users/export")
async def export_users(
    db: DBSession,
    _admin: RequireAdmin,
    status: UserStatus | None = None,
    role: Role | None = None,
    q: str | None = None,
) -> StreamingResponse:
    rows, _ = await list_paged(
        db,
        limit=10_000,
        offset=0,
        status=status,
        role=role,
        q=q,
        include_deleted=False,
    )

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        [
            "ID",
            "Email",
            "First Name",
            "Last Name",
            "Role",
            "Status",
            "IEEE Membership #",
            "IEEE Grade",
            "University",
            "Study Level",
            "Study Program",
            "Expected Graduation",
            "Profile Visibility",
            "Registered At",
        ]
    )
    for u in rows:
        writer.writerow(
            [
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                u.role.value,
                u.status.value,
                u.ieee_membership_number,
                u.ieee_grade or "",
                u.university,
                u.study_level.value if u.study_level else "",
                u.study_program or "",
                u.expected_graduation_year or "",
                u.profile_visibility.value,
                u.created_at.isoformat(),
            ]
        )

    buf.seek(0)
    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d")
    filename = f"ieee-sb-oulu-members-{timestamp}.csv"
    return StreamingResponse(
        buf,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/uploads", summary="Upload an image")
async def upload_image(
    _admin: RequireAdmin,
    file: Annotated[UploadFile, File()],
) -> UploadResponse:
    data = await file.read()
    # boto3 is blocking — keep it off the event loop.
    url = await run_in_threadpool(
        storage.upload, data, file.content_type or "application/octet-stream"
    )
    return UploadResponse(url=url)


@router.get("/audit")
async def list_audit(
    pagination: PaginationDep,
    db: DBSession,
    _admin: RequireAdmin,
    action: AuditAction | None = None,
    target_user_id: int | None = None,
) -> Page[AuditEntry]:
    from sqlalchemy import func

    stmt = select(AuditLog)
    count_stmt = select(func.count()).select_from(AuditLog)

    if action is not None:
        stmt = stmt.where(AuditLog.action == action)
        count_stmt = count_stmt.where(AuditLog.action == action)
    if target_user_id is not None:
        stmt = stmt.where(AuditLog.target_user_id == target_user_id)
        count_stmt = count_stmt.where(AuditLog.target_user_id == target_user_id)

    rows = (
        (
            await db.execute(
                stmt.order_by(AuditLog.created_at.desc())
                .limit(pagination.limit)
                .offset(pagination.offset)
            )
        )
        .scalars()
        .all()
    )
    total = (await db.execute(count_stmt)).scalar_one()

    items = [
        AuditEntry(
            id=r.id,
            actor_user_id=r.actor_user_id,
            action=r.action,
            target_user_id=r.target_user_id,
            metadata=r.audit_metadata,
            ip=str(r.ip) if r.ip else None,
            created_at=r.created_at,
        )
        for r in rows
    ]
    return Page(
        items=items,
        total=int(total),
        limit=pagination.limit,
        offset=pagination.offset,
    )
