"""Pydantic schemas for blog posts."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

PostCategory = Literal["workshop-recap", "tutorial", "branch-news", "tech-notes", "event-recap"]


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class TocHeading(BaseModel):
    id: str
    text: str
    level: int  # 2 or 3


class PostMeta(_CamelModel):
    id: int
    title: str
    slug: str
    excerpt: str
    category: PostCategory
    author: str
    author_initials: str
    author_role: str

    date: str  # human-display, e.g. "Feb 12, 2026"
    date_iso: str = Field(..., serialization_alias="dateISO")
    read_time: str  # "9 min read"
    tags: list[str]
    featured: bool = False
    cover_image_url: str | None = None
    event_slug: str | None = None


class PostFull(PostMeta):
    headings: list[TocHeading]
    body_html: str = Field(..., serialization_alias="bodyHtml")


class PostEdit(_CamelModel):
    """Raw, editable representation for the admin form (includes markdown source)."""

    id: int
    slug: str
    title: str
    excerpt: str
    body_md: str
    category: PostCategory
    tags: list[str]
    featured: bool
    cover_image_url: str | None = None
    event_slug: str | None = None
    published_on: date
    author_name: str
    author_initials: str
    author_role: str


class PostCreate(_CamelModel):
    title: str = Field(..., min_length=1, max_length=200)
    excerpt: str = Field(..., min_length=1)
    body_md: str = Field(..., min_length=1)
    category: PostCategory
    tags: list[str] = Field(default_factory=list)
    featured: bool = False
    cover_image_url: str | None = None
    event_slug: str | None = None
    published_on: date | None = None
    # Author fields default to the acting admin when omitted.
    author_name: str | None = None
    author_initials: str | None = None
    author_role: str | None = None


class PostUpdate(_CamelModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    excerpt: str | None = Field(default=None, min_length=1)
    body_md: str | None = Field(default=None, min_length=1)
    category: PostCategory | None = None
    tags: list[str] | None = None
    featured: bool | None = None
    cover_image_url: str | None = None
    event_slug: str | None = None
    published_on: date | None = None
    author_name: str | None = None
    author_initials: str | None = None
    author_role: str | None = None
