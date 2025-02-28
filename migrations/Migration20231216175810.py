async def up(connection):
    await connection.execute(
        'create table "product_periods_after_opening_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_periods_after_opening_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_periods_after_opening_tag_value_index" on "product_periods_after_opening_tag" ("value");',
    )

    await connection.execute(
        'alter table "product_periods_after_opening_tag" add constraint "product_periods_after_opening_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute('drop table if exists "product_owners_tag" cascade;')
