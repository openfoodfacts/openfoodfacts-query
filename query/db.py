import asyncpg
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

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

    LOG_LEVEL: str


settings = Settings()

# Make the log levels match the current ones from NestJS
log_name_to_level = {
    'debug': logging.DEBUG,
    'verbose': logging.INFO,
    'log': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR
}

# TODO: Could add coloured logging here
# TODO: Fiogure out how to use the same logger as FastAPI / uvicorn
logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] %(message)s', level=log_name_to_level[settings.LOG_LEVEL])



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
