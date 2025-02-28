async def up(connection):
    await connection.execute(
        'alter table "product" alter column "last_modified" type timestamptz using ("last_modified"::timestamptz);'
    )
    await connection.execute(
        'alter table "product" alter column "last_updated" type timestamptz using ("last_updated"::timestamptz);'
    )

    await connection.execute(
        'alter table "settings" alter column "last_modified" type timestamptz using ("last_modified"::timestamptz);'
    )
