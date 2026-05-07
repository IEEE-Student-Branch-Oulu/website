"""Markdown -> HTML + table-of-contents extraction.

Used by posts.service to populate `bodyHtml` and `headings` on
`BlogPostFull`. Keeping the parser shared in `core/` so any future
markdown surface (announcements, page content) can reuse it.
"""

from dataclasses import dataclass

from markdown_it import MarkdownIt
from markdown_it.token import Token
from slugify import slugify


@dataclass(frozen=True)
class Heading:
    id: str
    text: str
    level: int  # 2 or 3


@dataclass(frozen=True)
class RenderedMarkdown:
    html: str
    headings: list[Heading]


_md = MarkdownIt("commonmark", {"html": False, "breaks": False, "linkify": True}).enable(
    ["table", "strikethrough"]
)


def render(source: str) -> RenderedMarkdown:
    """Render markdown to HTML, tagging h2/h3 with slug ids and emitting a TOC."""
    tokens: list[Token] = _md.parse(source)
    headings: list[Heading] = []

    for i, tok in enumerate(tokens):
        if tok.type != "heading_open":
            continue
        level = int(tok.tag[1:])  # 'h2' -> 2
        if level not in (2, 3):
            continue
        inline = tokens[i + 1] if i + 1 < len(tokens) else None
        text = inline.content if inline and inline.type == "inline" else ""
        slug = slugify(text) or f"heading-{len(headings) + 1}"
        attrs = dict(tok.attrs or {})
        attrs["id"] = slug
        tok.attrs = attrs
        headings.append(Heading(id=slug, text=text, level=level))

    html = _md.renderer.render(tokens, _md.options, {})
    return RenderedMarkdown(html=html, headings=headings)
