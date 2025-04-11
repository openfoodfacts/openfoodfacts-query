"""Manages keeping the database schema up to date"""

import logging
import os
from importlib import import_module

from asyncpg import Connection

from query.config import config_settings

MIGRATIONS_TABLE = "mikro_orm_migrations"
MIGRATIONS_FOLDER = "query/migrations"

logger = logging.getLogger(__name__)


async def ensure_migration_table(transaction: Connection):
    """Create the migrations table if it doesn't already exist"""
    await transaction.execute(f"create schema if not exists {config_settings.SCHEMA};")
    await transaction.execute(f"SET search_path={config_settings.SCHEMA},public")
    await transaction.execute(
        f"ALTER ROLE {config_settings.POSTGRES_USER} SET search_path={config_settings.SCHEMA},public",
    )

    # Use the Mikro-ORM table to keep database compatibility
    await transaction.execute(
        f"""CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
        id serial4 PRIMARY KEY, 
        name varchar(255) NULL, 
        executed_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL
    )"""
    )


async def migrate_database(transaction: Connection):
    """Apply all necessary upgrade scripts to the database"""
    await ensure_migration_table(transaction)
    rows = await transaction.fetch(f"SELECT * FROM {MIGRATIONS_TABLE}")
    existing_migrations = [r["name"] for r in rows]
    for fname in sorted(os.listdir(MIGRATIONS_FOLDER)):
        if fname.endswith(".py") and not fname.startswith("__"):
            migration_name = fname.split(".")[0]
            if migration_name not in existing_migrations:
                logger.info(f"Applying {fname}")
                module = import_module(
                    f'{MIGRATIONS_FOLDER.replace("/",".")}.{migration_name}'
                )
                async with transaction.transaction():
                    await module.up(transaction)
                    await transaction.execute(
                        f"INSERT INTO {MIGRATIONS_TABLE} (name) VALUES ($1)",
                        migration_name,
                    )
