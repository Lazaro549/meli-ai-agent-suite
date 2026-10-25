from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    meli_base_url: str = "https://api.mercadolibre.com"
    meli_access_token: str = ""
    meli_app_id: str = ""
    meli_app_secret: str = ""
    meli_redirect_uri: str = "http://localhost:8000/callback"
    meli_site_id: str = "MLA"
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_session_token: str = ""
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    app_env: str = "development"
    log_level: str = "INFO"
    max_tokens: int = 1024
    temperature: float = 0.2
    request_timeout: float = 15.0
    max_retries: int = 2
    low_stock_threshold: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
