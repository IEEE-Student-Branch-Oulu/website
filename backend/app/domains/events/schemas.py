"""Pydantic schemas for events.

Field names are snake_case in Python; we emit camelCase JSON via aliases
so the frontend's `EventItem` interface needs no translation layer.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

EventType = Literal["workshop", "talk", "social", "meeting", "hackathon", "excursion"]
EventStatus = Literal["upcoming", "past", "ongoing"]


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class EventRead(_CamelModel):
    id: int
    title: str
    slug: str
    description: str

    date_iso: str = Field(..., serialization_alias="dateISO")
    date_display: str = Field(..., serialization_alias="dateDisplay")
    time_display: str = Field(..., serialization_alias="timeDisplay")

    location: str
    location_url: str | None = None

    type: EventType
    status: EventStatus

    rsvp_link: str | None = None
    capacity: int | None = None
    spots_left: int | None = None

    tags: list[str]

    speaker_name: str | None = None
    speaker_title: str | None = None
    is_highlighted: bool = False
    cover_image_url: str | None = None


class EventEdit(_CamelModel):
    """Raw, editable representation for the admin form."""

    id: int
    slug: str
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime | None = None
    location: str
    location_url: str | None = None
    type: EventType
    rsvp_link: str | None = None
    capacity: int | None = None
    speaker_name: str | None = None
    speaker_title: str | None = None
    is_highlighted: bool = False
    tags: list[str]
    cover_image_url: str | None = None


class EventCreate(_CamelModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    starts_at: datetime
    ends_at: datetime | None = None
    location: str = Field(..., min_length=1, max_length=200)
    location_url: str | None = None
    type: EventType
    rsvp_link: str | None = None
    capacity: int | None = Field(default=None, ge=0)
    speaker_name: str | None = None
    speaker_title: str | None = None
    is_highlighted: bool = False
    tags: list[str] = Field(default_factory=list)
    cover_image_url: str | None = None


class EventUpdate(_CamelModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1)
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    location: str | None = Field(default=None, min_length=1, max_length=200)
    location_url: str | None = None
    type: EventType | None = None
    rsvp_link: str | None = None
    capacity: int | None = Field(default=None, ge=0)
    speaker_name: str | None = None
    speaker_title: str | None = None
    is_highlighted: bool | None = None
    tags: list[str] | None = None
    cover_image_url: str | None = None
