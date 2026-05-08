"""Pydantic schemas for blog posts."""

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


class PostFull(PostMeta):
    headings: list[TocHeading]
    body_html: str = Field(..., serialization_alias="bodyHtml")
