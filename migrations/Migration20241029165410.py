async def up(connection):
    await connection.execute(
        'alter table "settings" rename column "last_modified" to "last_updated";'
    )
