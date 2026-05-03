from pathlib import Path

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(
        default="development",
        validation_alias=AliasChoices("APP_ENV", "ENVIRONMENT"),
    )
    debug: bool = Field(default=False, validation_alias=AliasChoices("APP_DEBUG"))

    api_host: str = "0.0.0.0"  # nosec B104
    api_port: int = 8000

    database_url: str = "postgresql+asyncpg://collabsta:collabsta@localhost:5432/collabsta"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "change-me"
    storage_path: str = "./data/uploads"

    @model_validator(mode="after")
    def validate_secret_key(self) -> "Settings":
        dev_envs = {"development", "dev", "local", "test", "testing"}
        if self.app_env.lower() not in dev_envs and self.secret_key == "change-me":  # nosec B105
            raise ValueError("SECRET_KEY must be changed outside development/test environments")
        return self


settings = Settings()
