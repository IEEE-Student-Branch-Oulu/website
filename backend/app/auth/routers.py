"""Auth endpoints: register, login, logout, me, verify, resend, forgot, reset, change."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response

from app.auth.dependencies import CurrentUser
from app.auth.models import AuditAction
from app.auth.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResendVerifyRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from app.auth.service import (
    change_password,
    forgot_password,
    login,
    register,
    resend_verification,
    reset_password,
    verify_email,
)
from app.auth.sessions import (
    create_session,
    delete_session_cookie,
    revoke_all_sessions,
    revoke_session,
    set_session_cookie,
)
from app.config import get_settings
from app.core.audit import record
from app.core.rate_limit import (
    FORGOT_LIMIT,
    LOGIN_LIMIT,
    REGISTER_LIMIT,
    RESEND_LIMIT,
    RESET_LIMIT,
    limiter,
)
from app.deps import DBSession
from app.domains.members.schemas import UserSelf

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
@limiter.limit(REGISTER_LIMIT)
async def register_endpoint(
    request: Request,
    body: RegisterRequest,
    db: DBSession,
) -> dict[str, str]:
    user = await register(
        db,
        email=body.email,
        password=body.password,
        first_name=body.first_name,
        last_name=body.last_name,
        ieee_membership_number=body.ieee_membership_number,
        ieee_grade=body.ieee_grade,
        university=body.university,
        study_level=body.study_level,
        study_program=body.study_program,
        expected_graduation_year=body.expected_graduation_year,
        profile_visibility=body.profile_visibility,
        consents=body.consents,
    )
    if user is not None:
        await record(
            db,
            action=AuditAction.register,
            actor_user_id=user.id,
            target_user_id=user.id,
            request=request,
        )
    await db.commit()
    return {"message": "Check your email to verify your account."}


@router.post("/login")
@limiter.limit(LOGIN_LIMIT)
async def login_endpoint(
    request: Request,
    body: LoginRequest,
    db: DBSession,
    response: Response,
) -> UserSelf:
    try:
        user = await login(db, email=body.email, password=body.password)
    except Exception:
        await record(
            db,
            action=AuditAction.login_failed,
            metadata={"email": body.email},
            request=request,
        )
        await db.commit()
        raise

    raw_token, _session = await create_session(
        db,
        user_id=user.id,
        user_agent=request.headers.get("user-agent"),
        ip=request.client.host if request.client else None,
    )
    await record(
        db,
        action=AuditAction.login,
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
    )
    await db.commit()

    set_session_cookie(response, raw_token, secure=not get_settings().is_dev)

    from app.domains.members.service import get_self_with_periods

    return await get_self_with_periods(db, user)


@router.post("/logout", status_code=204)
async def logout_endpoint(
    request: Request,
    db: DBSession,
    response: Response,
    user: CurrentUser,
) -> None:
    from app.auth.sessions import COOKIE_NAME, load_session

    raw_token = request.cookies.get(COOKIE_NAME)
    if raw_token:
        session = await load_session(db, raw_token)
        if session:
            await revoke_session(db, session.id)

    await record(
        db,
        action=AuditAction.logout,
        actor_user_id=user.id,
        request=request,
    )
    await db.commit()

    delete_session_cookie(response, secure=not get_settings().is_dev)


@router.get("/me")
async def me_endpoint(user: CurrentUser, db: DBSession) -> UserSelf:
    from app.domains.members.service import get_self_with_periods

    return await get_self_with_periods(db, user)


@router.post("/verify-email")
async def verify_email_endpoint(
    request: Request,
    body: VerifyEmailRequest,
    db: DBSession,
) -> dict[str, str]:
    await verify_email(db, raw_token=body.token)
    await db.commit()
    return {"message": "Email verified successfully."}


@router.post("/resend-verify", status_code=204)
@limiter.limit(RESEND_LIMIT)
async def resend_verify_endpoint(
    request: Request,
    body: ResendVerifyRequest,
    db: DBSession,
) -> None:
    await resend_verification(db, email=body.email)
    await db.commit()


@router.post("/forgot-password", status_code=204)
@limiter.limit(FORGOT_LIMIT)
async def forgot_password_endpoint(
    request: Request,
    body: ForgotPasswordRequest,
    db: DBSession,
) -> None:
    await forgot_password(db, email=body.email)
    await db.commit()


@router.post("/reset-password")
@limiter.limit(RESET_LIMIT)
async def reset_password_endpoint(
    request: Request,
    body: ResetPasswordRequest,
    db: DBSession,
) -> dict[str, str]:
    user = await reset_password(db, raw_token=body.token, new_password=body.password)
    await revoke_all_sessions(db, user.id)
    await record(
        db,
        action=AuditAction.password_change,
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
    )
    await db.commit()
    return {"message": "Password reset successfully. Please log in."}


@router.post("/change-password", status_code=204)
async def change_password_endpoint(
    request: Request,
    body: ChangePasswordRequest,
    db: DBSession,
    user: CurrentUser,
) -> None:
    await change_password(
        db,
        user=user,
        current_password=body.current_password,
        new_password=body.new_password,
    )

    from app.auth.sessions import COOKIE_NAME, load_session

    raw_token = request.cookies.get(COOKIE_NAME)
    current_session = None
    if raw_token:
        current_session = await load_session(db, raw_token)

    await revoke_all_sessions(
        db,
        user.id,
        except_session_id=current_session.id if current_session else None,
    )
    await record(
        db,
        action=AuditAction.password_change,
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
    )
    await db.commit()
