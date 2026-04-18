from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/voice_saas"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/voice_saas"

    OPENAI_API_KEY: Optional[str] = None
    WHISPER_MODEL: str = "base"

    UPLOAD_DIR: str = "/tmp/voice_saas_uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    REDIS_URL: str = "redis://localhost:6379/0"

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
