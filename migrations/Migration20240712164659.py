import query.repositories.products as products

async def up(connection):
    await connection.execute(
        'alter table "settings" alter column "last_modified" type timestamptz using ("last_modified"::timestamptz);'
    )
