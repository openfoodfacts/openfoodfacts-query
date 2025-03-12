from contextlib import asynccontextmanager
import asyncpg
import logging
from query.config import config_settings


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
