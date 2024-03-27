"""PyAqueduct Settings."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class to be read from the environment variables."""

    api_token: Optional[str] = None
