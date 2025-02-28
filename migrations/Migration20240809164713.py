async def up(connection):
    await connection.execute(
        'alter table "product" add column "revision" int null;',
    )
