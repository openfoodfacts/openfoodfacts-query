async def up(connection):
    await connection.execute(
        'alter table "product_ingredient" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredient" alter column "obsolete" drop not null;'
    )
