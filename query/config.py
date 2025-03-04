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


config_settings = ConfigSettings()

