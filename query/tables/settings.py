"""Global settings that are stored in the database"""

from datetime import datetime

from query.database import get_transaction


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
    

async def get_last_updated(transaction) -> datetime:
    """The most recent last_updated date for a product in the PostgreSQL database"""
    return await transaction.fetchval("SELECT last_updated FROM settings")


async def set_last_updated(transaction, last_updated):
    await transaction.execute("UPDATE settings SET last_updated = $1", last_updated)


async def get_last_message_id(transaction) -> str:
    """The last message id that was received from Redis. Used when resuming the Redis listener"""
    return (await transaction.fetchval("SELECT last_message_id FROM settings")) or "0"


async def set_last_message_id(transaction, message_id):
    await transaction.execute("UPDATE settings SET last_message_id = $1", message_id)
    
    
async def set_pre_migration_message_id():
    """Makes a note of the last Redis message_id before a data migration starts.
    Messages after this will bre re-played on the new version once the upgrade finishes"""
    # Use a separate transaction so that this doesn't block the current instance from updating last_message_id
    async with get_transaction() as transaction:
        await transaction.execute("UPDATE settings SET pre_migration_message_id = last_message_id WHERE pre_migration_message_id IS NULL")

 
async def apply_pre_migration_message_id():
    """Reset the last message id to what it was when the last upgrade started so that the messages can be
    replayed against the new database schema"""
    async with get_transaction() as transaction:
        await transaction.execute("UPDATE settings SET last_message_id = pre_migration_message_id, pre_migration_message_id = NULL WHERE pre_migration_message_id IS NOT NULL")
    