async def up(connection):
    await connection.execute(
        'alter table "product" add column "last_updated" timestamp null, add column "source" varchar(255) null;',
    )
