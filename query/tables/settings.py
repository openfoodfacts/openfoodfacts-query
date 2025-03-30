from datetime import datetime


async def create_table(connection):
    await connection.execute(
        "create table settings (id serial primary key, last_updated timestamptz null, last_message_id text null);",
    )
    await connection.execute(
        "INSERT INTO settings (last_updated) SELECT NULL WHERE NOT EXISTS (SELECT * FROM settings)",
    )


async def set_last_updated(connection, last_updated):
    await connection.execute("UPDATE settings SET last_updated = $1", last_updated)


async def get_last_updated(connection) -> datetime:
    return await connection.fetchval("SELECT last_updated FROM settings")


async def set_last_message_id(connection, message_id):
    await connection.execute("UPDATE settings SET last_message_id = $1", message_id)


async def get_last_message_id(connection) -> str:
    return (await connection.fetchval("SELECT last_message_id FROM settings")) or '0'
