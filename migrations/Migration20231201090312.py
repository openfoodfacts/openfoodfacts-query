async def up(connection):
    await connection.execute(
        'alter table "product_ingredient" alter column "percent" type text using ("percent"::text);',
    )
