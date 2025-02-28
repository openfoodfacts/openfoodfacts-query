async def up(connection):
    await connection.execute(
        'create table "settings" ("id" serial primary key, "last_modified" timestamp null);',
    )
