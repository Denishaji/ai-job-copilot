# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "AI Job Copilot Backend"
    app_version: str = "0.1.0"
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
