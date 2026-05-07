"""Slug helpers."""

from slugify import slugify as _slugify


def slugify(value: str) -> str:
    return str(_slugify(value, max_length=80, word_boundary=True))
