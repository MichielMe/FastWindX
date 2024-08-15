"""
Core configuration module for FastWindX.
"""

import logging
import secrets
from pathlib import Path
from typing import Any, List, Optional

from pydantic import AnyUrl, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings.

    These settings are loaded from environment variables.
    """

    PROJECT_NAME: str = "FastWindX"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080"]

    # Database settings
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "fastwindx"
    POSTGRES_PASSWORD: str = "fastwindx"
    POSTGRES_DB: str = "fastwindx"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Templates
    TEMPLATES_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "templates")

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        if self.SQLALCHEMY_DATABASE_URI:
            return self

        print(f"Assembling DB connection with data: {self.model_dump()}")

        required_fields = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_SERVER", "POSTGRES_DB"]
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Missing {field}")

        self.SQLALCHEMY_DATABASE_URI = AnyUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            path=f"/{self.POSTGRES_DB}",
        ).unicode_string()

        return self

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        print(f"Loaded settings: {self.model_dump()}")


settings = Settings()
