import asyncpg
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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


settings = Settings()


class Database:
    async def __aenter__(self):
        self.connection = await asyncpg.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST.split(":")[0],
            port=settings.POSTGRES_HOST.split(":")[-1],
        )
        return self.connection

    async def __aexit__(self, *_):
        await self.connection.close()
