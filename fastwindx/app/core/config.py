"""
Core configuration module for FastWindX.
"""

import logging
import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyUrl, field_validator
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

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        """
        Assemble the database connection string.
        """
        if isinstance(v, str):
            return v
        print(f"Assembling DB connection with data: {info.data}")
        url = AnyUrl.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"/{info.data.get('POSTGRES_DB') or ''}",
        ).unicode_string()
        logger.info(f"***********DATABASE URL: {url}")
        return url

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    # Templates
    TEMPLATES_DIR: Path = Path(__file__).parent.parent / "templates"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"Loaded settings: {self.model_dump()}")


settings = Settings()

# print(settings.model_dump())
