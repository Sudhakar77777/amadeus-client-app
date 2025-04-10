from functools import lru_cache
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env", env_file_encoding="utf-8"
    )
    amadeus_api_url: HttpUrl
    amadeus_api_key: str
    amadeus_api_secret: str
    amadeus_host: str


@lru_cache
def get_config() -> Settings:
    return Settings()


config = get_config()
