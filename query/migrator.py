"""Manages keeping the database schema up to date"""

import asyncio
import logging
import os
from importlib import import_module

from asyncpg import Connection

from query.config import config_settings
from query.database import get_transaction

MIGRATIONS_TABLE = "mikro_orm_migrations"
MIGRATIONS_FOLDER = "query/migrations"

logger = logging.getLogger("migrator")


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


async def migrate_database(apply=False):
    async with get_transaction() as transaction:
        """Apply all necessary upgrade scripts to the database"""
        logger.info("Checking if any migrations need to be applied")
        await ensure_migration_table(transaction)

        # Get the migrations that have already been run
        rows = await transaction.fetch(f"SELECT * FROM {MIGRATIONS_TABLE}")
        existing_migrations = [r["name"] for r in rows]

    # Migrations are stored in the migrations folder and are executed in alphabetical order
    migrations_to_run = []
    for fname in sorted(os.listdir(MIGRATIONS_FOLDER)):
        if fname.endswith(".py") and not fname.startswith("__"):
            migration_name = fname.split(".")[0]
            if migration_name not in existing_migrations:
                migrations_to_run.append(migration_name)

    if apply:
        for migration_name in migrations_to_run:
            logger.info(f"Applying {migration_name}")
            module = import_module(
                f'{MIGRATIONS_FOLDER.replace("/",".")}.{migration_name}'
            )
            # Each migration is run in its own transaction so that if one fails we don't
            # roll back all of them
            async with get_transaction() as transaction:
                # Each migration file just has to implement an "up" function that takes a transaction as a parameter
                await module.up(transaction)
                await transaction.execute(
                    f"INSERT INTO {MIGRATIONS_TABLE} (name) VALUES ($1)",
                    migration_name,
                )
    else:
        if migrations_to_run:
            logger.critical(
                f"The following migrations have not been run: {repr(migrations_to_run)}"
            )
            return False

        logger.info("All migrations are up to date")
    return True


if __name__ == "__main__":
    if asyncio.run(migrate_database(True)):
        logger.info("Migrations completed successfully")
