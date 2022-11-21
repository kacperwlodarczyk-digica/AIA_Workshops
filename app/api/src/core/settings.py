from functools import lru_cache
from pydantic import BaseSettings


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "AI Academy"
    API_PREFIX: str = "/api/v1"

    # For the Workshop purposes, we're allowing any origin to communicate with our API 
    CORS_ALLOWED_ORIGINS: list[str] = ["*"]
    
    DEVICE = "cpu"

    class Config:
        # More https://pydantic-docs.helpmanual.io/usage/settings/
        case_sensitive = True
        env_file = ".env"

@lru_cache
def load_settings() -> AppSettings:
    return AppSettings()