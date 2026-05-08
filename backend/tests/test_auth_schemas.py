"""Tests for auth request schema validation.

Verifies that Pydantic enforces field constraints at the API boundary:
password length, IEEE membership number format, graduation year range, etc.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
)


def _valid_register_data(**overrides: object) -> dict:
    base = {
        "email": "alice@example.com",
        "password": "secure-password-12",
        "firstName": "Alice",
        "lastName": "Smith",
        "ieeeMembershipNumber": "12345678",
        "consents": {"privacy": True, "terms": True},
    }
    base.update(overrides)
    return base


class TestRegisterRequest:
    def test_accepts_valid_minimal(self) -> None:
        req = RegisterRequest(**_valid_register_data())
        assert req.email == "alice@example.com"
        assert req.university == "University of Oulu"

    def test_password_too_short(self) -> None:
        with pytest.raises(ValidationError, match="String should have at least 12"):
            RegisterRequest(**_valid_register_data(password="short"))

    def test_ieee_number_must_be_digits(self) -> None:
        with pytest.raises(ValidationError, match="pattern"):
            RegisterRequest(**_valid_register_data(ieeeMembershipNumber="ABCD1234"))

    def test_ieee_number_length_bounds(self) -> None:
        with pytest.raises(ValidationError):
            RegisterRequest(**_valid_register_data(ieeeMembershipNumber="1234567"))
        with pytest.raises(ValidationError):
            RegisterRequest(**_valid_register_data(ieeeMembershipNumber="12345678901"))

    def test_ieee_number_8_9_10_digits_all_valid(self) -> None:
        for n in ("12345678", "123456789", "1234567890"):
            req = RegisterRequest(**_valid_register_data(ieeeMembershipNumber=n))
            assert req.ieee_membership_number == n

    def test_graduation_year_bounds(self) -> None:
        RegisterRequest(**_valid_register_data(expectedGraduationYear=2028))
        with pytest.raises(ValidationError, match="greater than or equal"):
            RegisterRequest(**_valid_register_data(expectedGraduationYear=1899))
        with pytest.raises(ValidationError, match="less than or equal"):
            RegisterRequest(**_valid_register_data(expectedGraduationYear=2101))

    def test_camel_case_aliases(self) -> None:
        req = RegisterRequest(**_valid_register_data(studyProgram="CS"))
        assert req.study_program == "CS"


class TestResetPasswordRequest:
    def test_password_too_short(self) -> None:
        with pytest.raises(ValidationError, match="12"):
            ResetPasswordRequest(token="abc", password="short")

    def test_valid(self) -> None:
        req = ResetPasswordRequest(token="abc", password="long-enough-pw!")
        assert req.token == "abc"


class TestChangePasswordRequest:
    def test_new_password_too_short(self) -> None:
        with pytest.raises(ValidationError, match="12"):
            ChangePasswordRequest(currentPassword="old-pw-12345!", newPassword="short")


class TestLoginRequest:
    def test_accepts_any_strings(self) -> None:
        req = LoginRequest(email="x", password="y")
        assert req.email == "x"
