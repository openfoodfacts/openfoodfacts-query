from contextlib import asynccontextmanager
import json
from typing import Any, AsyncGenerator
import asyncpg
import logging
from query.config import config_settings


@asynccontextmanager
async def database_connection() -> AsyncGenerator[asyncpg.Connection, Any]:
    connection = await asyncpg.connect(
        user=config_settings.POSTGRES_USER,
        password=config_settings.POSTGRES_PASSWORD,
        database=config_settings.POSTGRES_DB,
        host=config_settings.POSTGRES_HOST.split(":")[0],
        port=config_settings.POSTGRES_HOST.split(":")[-1],
    )
    try:
        await connection.set_type_codec(
            'jsonb',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )

        yield connection
    finally:
        await connection.close()

def get_rows_affected(response: str):
    parts = response.split(' ')
    if parts[0] == 'INSERT':
        return int(parts[2])
    return int(parts[1])
