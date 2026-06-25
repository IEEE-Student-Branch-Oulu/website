"""Image upload to S3 (or S3-compatible) object storage.

Used by the admin uploads endpoint to store images referenced from
post/event markdown and cover images. Objects are written with a random
key and a public-read ACL so the frontend can load them directly.
"""

from __future__ import annotations

import uuid
from functools import lru_cache

import boto3

from app.config import get_settings
from app.core.errors import DomainError

# content-type -> file extension
ALLOWED_TYPES: dict[str, str] = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
}

MAX_BYTES = 8 * 1024 * 1024  # 8 MB


class StorageError(DomainError):
    """Raised when an upload cannot be completed."""

    status_code = 400
    title = "Upload Failed"


@lru_cache
def _client():  # type: ignore[no-untyped-def]
    settings = get_settings()
    if not settings.s3_bucket:
        raise StorageError("Image storage is not configured.")
    return boto3.client(
        "s3",
        region_name=settings.s3_region,
        endpoint_url=settings.s3_endpoint_url or None,
        aws_access_key_id=settings.aws_access_key_id or None,
        aws_secret_access_key=settings.aws_secret_access_key or None,
    )


def _public_url(key: str) -> str:
    settings = get_settings()
    if settings.s3_public_base_url:
        return f"{settings.s3_public_base_url.rstrip('/')}/{key}"
    if settings.s3_endpoint_url:
        return f"{settings.s3_endpoint_url.rstrip('/')}/{settings.s3_bucket}/{key}"
    return f"https://{settings.s3_bucket}.s3.{settings.s3_region}.amazonaws.com/{key}"


def upload(data: bytes, content_type: str) -> str:
    """Validate and store ``data``; return the public URL."""
    ext = ALLOWED_TYPES.get(content_type)
    if ext is None:
        raise StorageError(f"Unsupported image type: {content_type!r}.")
    if len(data) > MAX_BYTES:
        raise StorageError("Image exceeds the 8 MB limit.")

    settings = get_settings()
    key = f"uploads/{uuid.uuid4().hex}.{ext}"
    # No ACL: modern buckets use "Bucket owner enforced" ownership, which
    # rejects object ACLs. Public read is granted via a bucket policy instead.
    _client().put_object(
        Bucket=settings.s3_bucket,
        Key=key,
        Body=data,
        ContentType=content_type,
    )
    return _public_url(key)
