"""Tests for utilities in app/core/."""

from app.core.errors import (
    AuthenticationError,
    ConflictError,
    DomainError,
    NotFoundError,
    PermissionDeniedError,
    _problem,
    _status_title,
)
from app.core.pagination import Page
from app.core.slug import slugify
from app.deps import Pagination, pagination_params


class TestSlugify:
    def test_basic(self) -> None:
        assert slugify("Hello World") == "hello-world"

    def test_punctuation_stripped(self) -> None:
        assert slugify("How We Built a Working Radar System!") == (
            "how-we-built-a-working-radar-system"
        )

    def test_max_length_word_boundary(self) -> None:
        result = slugify("a" * 200)
        assert len(result) <= 80


class TestDomainErrors:
    def test_not_found_defaults(self) -> None:
        err = NotFoundError()
        assert err.status_code == 404
        assert err.detail == "Not Found"

    def test_not_found_custom_detail(self) -> None:
        err = NotFoundError("Event 'foo' not found.")
        assert err.detail == "Event 'foo' not found."

    def test_authentication_error(self) -> None:
        err = AuthenticationError("Bad token.")
        assert err.status_code == 401
        assert err.detail == "Bad token."

    def test_permission_denied_error(self) -> None:
        err = PermissionDeniedError()
        assert err.status_code == 403
        assert err.detail == "Forbidden"

    def test_conflict_error(self) -> None:
        err = ConflictError("Already exists.")
        assert err.status_code == 409

    def test_base_domain_error_defaults(self) -> None:
        err = DomainError()
        assert err.status_code == 500
        assert err.detail == "Internal Server Error"

    def test_domain_error_is_exception(self) -> None:
        assert issubclass(DomainError, Exception)


class TestProblemResponse:
    def test_problem_json_structure(self) -> None:
        resp = _problem(status=404, title="Not Found", detail="gone")
        assert resp.status_code == 404
        assert resp.media_type == "application/problem+json"

    def test_status_title_known_codes(self) -> None:
        assert _status_title(400) == "Bad Request"
        assert _status_title(401) == "Unauthorized"
        assert _status_title(403) == "Forbidden"
        assert _status_title(404) == "Not Found"
        assert _status_title(409) == "Conflict"
        assert _status_title(422) == "Unprocessable Entity"
        assert _status_title(500) == "Internal Server Error"

    def test_status_title_unknown_code(self) -> None:
        assert _status_title(418) == "Error"


class TestPage:
    def test_page_construction(self) -> None:
        page = Page(items=["a", "b"], total=10, limit=5, offset=0)
        assert page.items == ["a", "b"]
        assert page.total == 10

    def test_page_empty(self) -> None:
        page = Page(items=[], total=0, limit=20, offset=0)
        assert page.items == []


class TestPagination:
    def test_defaults(self) -> None:
        p = pagination_params()
        assert p.limit == 20
        assert p.offset == 0

    def test_custom_values(self) -> None:
        p = pagination_params(limit=50, offset=10)
        assert p.limit == 50
        assert p.offset == 10

    def test_frozen(self) -> None:
        p = Pagination(limit=5, offset=0)
        import dataclasses

        assert dataclasses.is_dataclass(p)
