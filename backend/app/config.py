import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file_path() -> Path:
    """Get the path to the .env file, checking multiple locations."""
    # Check for .env in the backend directory first
    backend_env = Path(__file__).parent.parent / ".env"
    if backend_env.exists():
        return backend_env
    # Fall back to .env in the current working directory
    return Path(".env")


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "CC Video"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/cc_video.db"

    # Authentication
    SECRET_KEY: str = "development-secret-key-change-in-production-32ch"  # Default for development
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=str(get_env_file_path()),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
