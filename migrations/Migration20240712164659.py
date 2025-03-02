import query.repositories.product as product

async def up(connection):
    await connection.execute(
        'alter table "settings" alter column "last_modified" type timestamptz using ("last_modified"::timestamptz);'
    )
