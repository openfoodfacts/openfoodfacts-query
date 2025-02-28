async def up(connection):
    await connection.execute(
        'create table "product_ingredient" ("product_id" uuid not null, "sequence" text not null, "parent_product_id" uuid null, "parent_sequence" text null, "ingredient_text" text null, "id" text null, "ciqual_food_code" text null, "percent_min" double precision null, "percent" double precision null, "percent_max" double precision null, "percent_estimate" double precision null, "data" json null, "obsolete" boolean not null default false, constraint "product_ingredient_pkey" primary key ("product_id", "sequence"));',
    )
    await connection.execute(
        'create index "product_ingredient_parent_product_id_parent_sequence_index" on "product_ingredient" ("parent_product_id", "parent_sequence");',
    )

    await connection.execute(
        'alter table "product_ingredient" add constraint "product_ingredient_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
    await connection.execute(
        'alter table "product_ingredient" add constraint "product_ingredient_parent_product_id_parent_sequence_foreign" foreign key ("parent_product_id", "parent_sequence") references "product_ingredient" ("product_id", "sequence") on update cascade on delete set null;',
    )

    await connection.execute(
        'ALTER TABLE query.product ALTER COLUMN "data" TYPE json USING "data"::text::json;',
    )

    await connection.execute(
        'alter table "product" add column "ingredients_without_ciqual_codes_count" int null, add column "ingredients_count" int null;',
    )
