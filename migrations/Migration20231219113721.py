async def up(connection):
    await connection.execute(
        'create table "product_ingredients_ntag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_ntag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_ingredients_ntag_value_index" on "product_ingredients_ntag" ("value");',
    )

    await connection.execute(
        'alter table "product_ingredients_ntag" add constraint "product_ingredients_ntag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
