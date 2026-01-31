from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    neon_db_url: str

    # Better Auth settings
    better_auth_secret: str
    better_auth_url: str

    # Cohere API settings
    cohere_api_key: str

    # Application settings
    debug: bool = False
    log_level: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()