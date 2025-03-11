from contextlib import asynccontextmanager
import asyncpg
import logging
from query.config import config_settings

# Make the log levels match the current ones from NestJS
log_name_to_level = {
    'debug': logging.DEBUG,
    'verbose': logging.INFO,
    'log': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR
}

# TODO: Could add coloured logging here
# TODO: Figure out how to use the same logger as FastAPI / uvicorn
logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] %(message)s', level=log_name_to_level[config_settings.LOG_LEVEL])


@asynccontextmanager
async def database_connection():
    connection = await asyncpg.connect(
        user=config_settings.POSTGRES_USER,
        password=config_settings.POSTGRES_PASSWORD,
        database=config_settings.POSTGRES_DB,
        host=config_settings.POSTGRES_HOST.split(":")[0],
        port=config_settings.POSTGRES_HOST.split(":")[-1],
    )
    try:
        yield connection
    finally:
        await connection.close()
