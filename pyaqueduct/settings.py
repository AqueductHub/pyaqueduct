"""PyAqueduct Settings."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_token: Optional[str] = None


settings = Settings()
