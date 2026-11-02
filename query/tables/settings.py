"""Global settings that are stored in the database"""

import logging

import asyncpg

from query.database import get_transaction

logger = logging.getLogger(__name__)


async def create_table(transaction):
    await transaction.execute(
        "create table settings (id serial primary key, last_updated timestamptz null, last_message_id text null);",
    )
    await transaction.execute(
        "INSERT INTO settings (last_updated) SELECT NULL WHERE NOT EXISTS (SELECT * FROM settings)",
    )


async def add_pre_migration_message_id(transaction):
    await transaction.execute(
        "alter table settings add column pre_migration_message_id text null;",
    )


async def add_bulk_message_id(transaction):
    await transaction.execute(
        """alter table settings add column last_bulk_message_id text null,
            add column pre_migration_bulk_message_id text null;""",
    )


def bulk_suffix(is_bulk: bool) -> str:
    return "bulk_" if is_bulk else ""


async def get_last_message_id(transaction, is_bulk = False) -> str:
    """The last message id that was received from Redis. Used when resuming the Redis listener"""
    return (await transaction.fetchval(f"SELECT last_{bulk_suffix(is_bulk)}message_id FROM settings")) or "0"


async def set_last_message_id(transaction, message_id, is_bulk = False):
    await transaction.execute(f"UPDATE settings SET last_{bulk_suffix(is_bulk)}message_id = $1", message_id)


async def set_pre_migration_message_id():
    """Makes a note of the last Redis message_id before a data migration starts.
    Messages after this will be replayed on the new version once the upgrade finishes
    """
    logger.info("Waiting for imports to finish before starting migrations")

    # Use a separate transaction so that this doesn't block the current instance from updating last_message_id
    # Also need bulk update separate as that column may not exist yet
    for is_bulk in [False, True]:
        column_name = f"pre_migration_{bulk_suffix(is_bulk)}message_id"
        async with get_transaction() as transaction:
            try:
                setting = await transaction.fetch(
                    f"UPDATE settings SET {column_name} = last_{bulk_suffix(is_bulk)}message_id WHERE {column_name} IS NULL RETURNING {column_name}"
                )
                if len(setting) == 1:
                    logger.info(
                        f"Will resume { 'bulk ' if is_bulk else '' }messages at id: {setting[0][column_name]}"
                    )
            except asyncpg.PostgresError as sql_error:
                # This is expected if the setting table hasn't been created yet
                logger.warning(f"Not able to set {column_name}: {sql_error}")


async def apply_pre_migration_message_id():
    """Reset the last message id to what it was when the last upgrade started so that the messages can be
    replayed against the new database schema"""
    async with get_transaction() as transaction:
        for is_bulk in [False, True]:
            column_name = f"last_{bulk_suffix(is_bulk)}message_id"
            setting = await transaction.fetch(
                f"UPDATE settings SET {column_name} = pre_migration_{bulk_suffix(is_bulk)}message_id, pre_migration_{bulk_suffix(is_bulk)}message_id = NULL WHERE pre_migration_{bulk_suffix(is_bulk)}message_id IS NOT NULL RETURNING {column_name}"
            )
            if len(setting) == 1:
                logger.info(f"Resuming { 'bulk ' if is_bulk else '' }messages from id: {setting[0][column_name]}")


async def acquire_import_lock(transaction) -> bool:
    """Check if we can start an import or if a migration has just finished. Locks the settings table
    if successful to prevent other imports and migrations from running concurrently"""
    pre_migration_message_id = await transaction.fetchval(
        "SELECT pre_migration_message_id FROM settings FOR UPDATE"
    )
    return not pre_migration_message_id
