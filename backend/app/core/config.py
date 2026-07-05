from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration, loaded from environment / .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: str = ""
    model_name: str = "claude-sonnet-5"
    temperature: float = 0.7
    max_revisions: int = 2
    eval_threshold: float = 7.0
    db_path: str = "./data/app.db"
    log_path: str = "./logs/agent.log"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
