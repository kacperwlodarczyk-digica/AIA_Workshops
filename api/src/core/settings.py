from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "AI Academy"
    API_VERSION_PREFIX: str = "/v1"
    DATA_LOCAL_DIR = Path(__file__).parents[3] / "data"

    # For the Workshop purposes, we're allowing any origin to communicate with our API
    CORS_ALLOWED_ORIGINS: list[str] = ["*"]

    # AWS
    REGION: str
    BUCKET_NAME: str
    MODEL_DATA_LOCATION_S3: str
    MODEL_FILE_NAME: str
    CLASS_NAMES_FILE_NAME: str
    # Local data path

    class Config:
        # More https://pydantic-docs.helpmanual.io/usage/settings/
        case_sensitive = True
        env_file = "env"


@lru_cache
def load_settings() -> AppSettings:
    return AppSettings()
