# app\core\settings.py
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = True

    DROPBOX_ACCESS_TOKEN: str | None = None
    DROPBOX_REFRESH_TOKEN: str | None = None
    DROPBOX_APP_KEY: str | None = None
    DROPBOX_APP_SECRET: str | None = None

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
        )
        env_file_encoding = "utf-8"


settings = Settings()
