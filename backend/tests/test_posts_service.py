"""Pure-logic tests for posts: markdown rendering and meta mapping."""

from datetime import date

from app.core.markdown import render
from app.domains.posts.models import Post
from app.domains.posts.service import to_meta


def _post(**overrides: object) -> Post:
    base = Post(
        id=1,
        title="Sample",
        slug="sample",
        excerpt="ex",
        body_md="## Hi\n\ntext",
        category="tutorial",
        author_name="A B",
        author_initials="AB",
        author_role="Member",
        published_on=date(2026, 2, 12),
        read_minutes=9,
        tags=["x"],
        featured=False,
    )
    for k, v in overrides.items():
        setattr(base, k, v)
    return base


class TestMarkdownRender:
    def test_emits_h2_with_id_and_heading(self) -> None:
        rendered = render("## Background\n\nbody")
        assert "<h2" in rendered.html
        assert 'id="background"' in rendered.html
        assert rendered.headings[0].id == "background"
        assert rendered.headings[0].level == 2
        assert rendered.headings[0].text == "Background"

    def test_h3_collected(self) -> None:
        rendered = render("## A\n\n### B\n\nc")
        levels = [h.level for h in rendered.headings]
        assert levels == [2, 3]

    def test_h1_and_h4_skipped(self) -> None:
        rendered = render("# top\n\n## a\n\n#### deep")
        ids = [h.id for h in rendered.headings]
        assert ids == ["a"]


class TestToMeta:
    def test_date_and_read_time_format(self) -> None:
        meta = to_meta(_post())
        assert meta.date == "Feb 12, 2026"
        assert meta.date_iso == "2026-02-12"
        assert meta.read_time == "9 min read"
        assert meta.author == "A B"
        assert meta.tags == ["x"]
