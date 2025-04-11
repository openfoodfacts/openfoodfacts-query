"""Global settings that are stored in the database"""

from datetime import datetime


async def create_table(transaction):
    await transaction.execute(
        "create table settings (id serial primary key, last_updated timestamptz null, last_message_id text null);",
    )
    await transaction.execute(
        "INSERT INTO settings (last_updated) SELECT NULL WHERE NOT EXISTS (SELECT * FROM settings)",
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
