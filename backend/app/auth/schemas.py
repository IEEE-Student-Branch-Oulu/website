"""Request/response schemas for auth endpoints."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.domains.members.models import StudyLevel, Visibility


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class RegisterRequest(_CamelModel):
    email: str = Field(max_length=254)
    password: str = Field(min_length=12)
    first_name: str = Field(max_length=80)
    last_name: str = Field(max_length=80)
    ieee_membership_number: str = Field(min_length=8, max_length=10, pattern=r"^\d{8,10}$")
    ieee_grade: str | None = Field(default=None, max_length=40)
    university: str = Field(default="University of Oulu", max_length=120)
    study_level: StudyLevel | None = None
    study_program: str | None = Field(default=None, max_length=120)
    expected_graduation_year: int | None = Field(default=None, ge=1900, le=2100)
    profile_visibility: Visibility = Visibility.private
    consents: dict[str, Any]


class LoginRequest(_CamelModel):
    email: str
    password: str


class VerifyEmailRequest(_CamelModel):
    token: str


class ResendVerifyRequest(_CamelModel):
    email: str


class ForgotPasswordRequest(_CamelModel):
    email: str


class ResetPasswordRequest(_CamelModel):
    token: str
    password: str = Field(min_length=12)


class ChangePasswordRequest(_CamelModel):
    current_password: str
    new_password: str = Field(min_length=12)
