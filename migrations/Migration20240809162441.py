async def up(connection):
    await connection.execute(
        'create index "product_creator_index" on "product" ("creator");'
    )
    await connection.execute(
        'create index "product_owners_tags_index" on "product" ("owners_tags");'
    )
