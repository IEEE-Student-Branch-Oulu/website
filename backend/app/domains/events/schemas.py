"""Pydantic schemas for events.

Field names are snake_case in Python; we emit camelCase JSON via aliases
so the frontend's `EventItem` interface needs no translation layer.
"""

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
