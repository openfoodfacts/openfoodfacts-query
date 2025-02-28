async def up(connection):
    await connection.execute(
        'create table "product_codes_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_codes_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_codes_tag_value_index" on "product_codes_tag" ("value");',
    )

    await connection.execute(
        'create table "product_data_quality_errors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_errors_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_data_quality_errors_tag_value_index" on "product_data_quality_errors_tag" ("value");',
    )

    await connection.execute(
        'create table "product_data_quality_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_data_quality_tag_value_index" on "product_data_quality_tag" ("value");',
    )

    await connection.execute(
        'create table "product_editors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_editors_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_editors_tag_value_index" on "product_editors_tag" ("value");',
    )

    await connection.execute(
        'create table "product_ingredients_original_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_original_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_ingredients_original_tag_value_index" on "product_ingredients_original_tag" ("value");',
    )

    await connection.execute(
        'create table "product_keywords_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_keywords_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_keywords_tag_value_index" on "product_keywords_tag" ("value");',
    )

    await connection.execute(
        'create table "product_stores_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_stores_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_stores_tag_value_index" on "product_stores_tag" ("value");',
    )

    await connection.execute(
        'alter table "product_codes_tag" add constraint "product_codes_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_data_quality_tag" add constraint "product_data_quality_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_editors_tag" add constraint "product_editors_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_ingredients_original_tag" add constraint "product_ingredients_original_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_keywords_tag" add constraint "product_keywords_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_stores_tag" add constraint "product_stores_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
