"""Application settings — one flat class, one .env file."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Literal["dev", "test", "prod"] = "dev"
    timezone: str = "Europe/Helsinki"

    # Database
    database_url: str = "postgresql+asyncpg://ieee:ieee@localhost:5432/ieee"
    database_echo: bool = False

    # CORS — comma-separated origins
    cors_origins: str = "http://localhost:3000"

    # Auth
    auth_secret_key: str = "change-me"

    # Email
    email_backend: Literal["console", "memory", "resend"] = "console"
    email_from: str = "IEEE SB Oulu <noreply@ieee-oulu.fi>"
    email_resend_api_key: str = ""

    # Public-facing URL (used in email links)
    public_base_url: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"


@lru_cache
def get_settings() -> Settings:
    return Settings()
