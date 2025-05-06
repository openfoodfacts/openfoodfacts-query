"""Manages PostgreSQL database connections and any specific helper functions"""

import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import asyncpg

from .config import config_settings

logger = logging.getLogger(__name__)


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
        async with connection.transaction():
            yield connection
    finally:
        await connection.close()


def get_rows_affected(response: str):
    """Extracts the rows affected from the standard PostgreSQL response"""
    parts = response.split(" ")
    if parts[0] == "INSERT":
        return int(parts[2])
    return int(parts[1])


async def create_record(transaction, table_name, **params):
    """This is mainly used for creating test data. The columns to populate are specified as keyword parameters and the full record is returned"""
    statement = f"INSERT INTO {table_name} ({','.join(params.keys())}) VALUES ({','.join(f'${i + 1}' for i in range(len(params)))}) RETURNING *"
    return await transaction.fetchrow(statement, *params.values())


def strip_nuls(enumerable: dict | list, context):
    """PostgreSQL doesn't like nuls in text fields, including JSON. The context is used for error logging"""
    enumeration = (
        enumerable.items() if isinstance(enumerable, dict) else enumerate(enumerable)
    )
    for key, value in enumeration:
        if isinstance(value, str) and "\0" in value:
            logger.warning(f"{context}: Nuls stripped from {key}: {value}")
            enumerable[key] = value.replace("\0", "")
