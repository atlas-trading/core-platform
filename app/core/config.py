from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """application configuration.

    - loads values from .env and environment variables via pydantic settings
    - includes common settings for fastapi, db, redis, auth, and access control
    """

    # app
    app_name: str = "Atlas Trading Platform"
    environment: str = Field(default="local", description="Deployment environment (local|dev|prod)")
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # database / cache / broker
    database_url: str = "sqlite+aiosqlite:///./atlas.db"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = Field(default_factory=lambda: "redis://localhost:6379/1")
    celery_result_backend: str = Field(default_factory=lambda: "redis://localhost:6379/2")

    # dashboard access control
    allowed_dashboard_cidrs: list[str] = Field(
        default_factory=list,
        description="CIDR list allowed to access dashboard (e.g., Tailscale subnets or node IP ranges).",
    )
    dashboard_basic_auth_user: str | None = None
    dashboard_basic_auth_password: str | None = None

    # exchange api keys (ccxt)
    binance_api_key: str | None = None
    binance_api_secret: str | None = None
    bybit_api_key: str | None = None
    bybit_api_secret: str | None = None

    # risk parameters (example)
    max_position_usd: float = 10000.0
    max_order_usd: float = 2000.0

    model_config = SettingsConfigDict(
        env_file=(Path.cwd() / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


settings = Settings()
