"""Manages PostgreSQL database connections and any specific helper functions"""

import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import asyncpg

from query.config import config_settings

logger = logging.getLogger(__name__)

pool: asyncpg.Pool = None


@asynccontextmanager
async def database_lifespan():
    """Lifespan handler for creating the database connection pool"""
    try:
        pool = await create_connection_pool()
        yield
    finally:
        await pool.close()


async def init_connection(connection: asyncpg.Connection):
    """Automatically configures codecs on every new physical pool connection."""
    await set_type_codec(connection)


async def set_type_codec(connection):
    await connection.set_type_codec(
        "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )


def get_db_config():
    """Returns the database configuration as a dict"""
    return {
        "user": config_settings.POSTGRES_USER,
        "password": config_settings.POSTGRES_PASSWORD,
        "database": config_settings.POSTGRES_DB,
        "host": config_settings.POSTGRES_HOST.split(":")[0],
        "port": config_settings.POSTGRES_HOST.split(":")[-1],
    }


async def create_connection_pool():
    """Creates a global connection pool to the PostgreSQL database"""
    global pool
    pool = await asyncpg.create_pool(
        **get_db_config(),
        init=init_connection,
        min_size=5,  # Keeps 5 connections warm and ready
        max_size=20,  # Limits physical connections to a maximum of 20
        # Crucial parameters for long-running pools
        max_queries=50000,  # Rebuilds a connection after 50k queries to prevent memory leaks
        max_inactive_connection_lifetime=300.0,  # Closes connections that sit idle for more than 5 minutes
        command_timeout=60.0,  # Fails safely if a query hangs for over 60 seconds
    )
    return pool


@asynccontextmanager
async def get_transaction() -> AsyncGenerator[asyncpg.Connection, Any]:
    if pool:
        async with pool.acquire() as connection:
            async with connection.transaction():
                yield connection
    else:
        # During migrations we don't start the pool as pooled connections might not contain the search_path, etc.
        connection: asyncpg.Connection = await asyncpg.connect(**get_db_config())
        try:
            await set_type_codec(connection)
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
    if not enumerable:
        return

    """PostgreSQL doesn't like nuls in text fields, including JSON. The context is used for error logging"""
    enumeration = (
        enumerable.items() if isinstance(enumerable, dict) else enumerate(enumerable)
    )
    for key, value in enumeration:
        value_type = type(value)
        if value_type is str and "\0" in value:
            logger.warning(
                f"{context}: Nuls stripped from {key}: {value}".replace(
                    "\r\n", ""
                ).replace("\n", "")
            )
            enumerable[key] = value.replace("\0", "")
        elif value_type is list or value_type is dict:
            strip_nuls(value, f"{context}.{key}")
