async def up(connection):
    await connection.execute(
        'alter table "settings" add column "last_message_id" text null;',
    )
