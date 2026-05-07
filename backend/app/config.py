"""Application settings, loaded from environment / `.env`.

Nested config groups (`db`, `cors`, `auth`) keep related variables together
and give us a clear extension point when auth lands.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    url: str = "postgresql+asyncpg://ieee:ieee@localhost:5432/ieee"
    echo: bool = False


class CORSSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CORS_")

    origins: list[str] = ["http://localhost:3000"]


class AuthSettings(BaseSettings):
    """Placeholder. Real auth lands in a follow-up plan."""

    model_config = SettingsConfigDict(env_prefix="AUTH_")

    secret_key: str = "change-me"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    env: Literal["dev", "test", "prod"] = "dev"
    api_prefix: str = "/api/v1"
    timezone: str = "Europe/Helsinki"

    # Convenience top-level mirror of DATABASE_URL — many platforms set it directly.
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    cors_origins_raw: str | None = Field(default=None, alias="CORS_ORIGINS")

    db: DBSettings = Field(default_factory=DBSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)

    def model_post_init(self, _context: object) -> None:
        if self.database_url:
            self.db.url = self.database_url
        if self.cors_origins_raw:
            self.cors.origins = [o.strip() for o in self.cors_origins_raw.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
