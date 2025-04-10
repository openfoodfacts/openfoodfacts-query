import json
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import asyncpg

from query.config import config_settings


@asynccontextmanager
async def get_transaction() -> AsyncGenerator[asyncpg.Connection, Any]:
    connection: asyncpg.Connection = await asyncpg.connect(
        user=config_settings.POSTGRES_USER,
        password=config_settings.POSTGRES_PASSWORD,
        database=config_settings.POSTGRES_DB,
        host=config_settings.POSTGRES_HOST.split(":")[0],
        port=config_settings.POSTGRES_HOST.split(":")[-1],
    )
    try:
        await connection.set_type_codec(
            "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
        )
        # TODO: Test that transactions are rolled back on error but connection is still closed
        async with connection.transaction():
            yield connection
    finally:
        await connection.close()


def get_rows_affected(response: str):
    parts = response.split(" ")
    if parts[0] == "INSERT":
        return int(parts[2])
    return int(parts[1])


async def create_record(transaction, table_name, returning=None, **params):
    """ " This is mainly used for creating test data"""
    statement = f"INSERT INTO {table_name} ({','.join(params.keys())}) VALUES ({','.join(f'${i + 1}' for i in range(len(params)))}) RETURNING *"
    return await transaction.fetchrow(statement, *params.values())
