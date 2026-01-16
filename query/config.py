"""Configuration information loaded from environment variables and / or .env files"""

import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SCHEMA: str = "query"
    VIEW_USER: str = "viewer"
    VIEW_PASSWORD: str = "off"

    MONGO_URI: str

    REDIS_URL: str

    LOG_LEVEL: str

    SKIP_DATA_MIGRATIONS: bool = False

    # used to compute hmac
    APP_SECRET_KEY: str


config_settings = ConfigSettings()

# Make the log levels match the current ones from NestJS
log_name_to_level = {
    "verbose": logging.NOTSET,
    "debug": logging.DEBUG,
    "log": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
}

# Could add coloured logging here
logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    level=log_name_to_level[config_settings.LOG_LEVEL],
)
