async def up(connection):
    await connection.execute(
        'alter table "product" rename column "last_updated" to "last_processed";'
    )
    await connection.execute(
        'alter table "product" rename column "last_modified" to "last_updated";'
    )
    await connection.execute(
        'alter table "settings" rename column "last_modified" to "last_updated";'
    )
    await connection.execute(
        'alter table "product" add column "process_id" bigint null;'
    )
    await connection.execute(
        'create index "product_process_id_index" on "product" ("process_id");'
    )
    await connection.execute('drop index "product_last_update_id_index";')
    await connection.execute('alter table "product" drop column "last_update_id";')
