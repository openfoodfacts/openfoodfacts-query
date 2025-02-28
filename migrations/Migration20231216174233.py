async def up(connection):
    await connection.execute(
        'create table "product_categories_properites_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_categories_properites_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_categories_properites_tag_value_index" on "product_categories_properites_tag" ("value");',
    )

    await connection.execute(
        'create table "product_checkers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_checkers_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_checkers_tag_value_index" on "product_checkers_tag" ("value");',
    )

    await connection.execute(
        'create table "product_cities_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_cities_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_cities_tag_value_index" on "product_cities_tag" ("value");',
    )

    await connection.execute(
        'create table "product_correctors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_correctors_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_correctors_tag_value_index" on "product_correctors_tag" ("value");',
    )

    await connection.execute(
        'create table "product_data_quality_bugs_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_bugs_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_data_quality_bugs_tag_value_index" on "product_data_quality_bugs_tag" ("value");',
    )

    await connection.execute(
        'create table "product_data_quality_warnings_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_warnings_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_data_quality_warnings_tag_value_index" on "product_data_quality_warnings_tag" ("value");',
    )

    await connection.execute(
        'create table "product_debug_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_debug_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_debug_tag_value_index" on "product_debug_tag" ("value");',
    )

    await connection.execute(
        'create table "product_food_groups_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_food_groups_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_food_groups_tag_value_index" on "product_food_groups_tag" ("value");',
    )

    await connection.execute(
        'create table "product_informers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_informers_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_informers_tag_value_index" on "product_informers_tag" ("value");',
    )

    await connection.execute(
        'create table "product_ingredients_analysis_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_analysis_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_ingredients_analysis_tag_value_index" on "product_ingredients_analysis_tag" ("value");',
    )

    await connection.execute(
        'create table "product_ingredients_from_palm_oil_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_ingredients_from_palm_oil_tag_value_index" on "product_ingredients_from_palm_oil_tag" ("value");',
    )

    await connection.execute(
        'create table "product_ingredients_that_may_be_from_palm_oil_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_ingredients_that_may_be_from_palm_oil_tag_value_index" on "product_ingredients_that_may_be_from_palm_oil_tag" ("value");',
    )

    await connection.execute(
        'create table "product_latest_image_dates_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_latest_image_dates_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_latest_image_dates_tag_value_index" on "product_latest_image_dates_tag" ("value");',
    )

    await connection.execute(
        'create table "product_nutrient_levels_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nutrient_levels_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_nutrient_levels_tag_value_index" on "product_nutrient_levels_tag" ("value");',
    )

    await connection.execute(
        'create table "product_nutriscore2021tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nutriscore2021tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_nutriscore2021tag_value_index" on "product_nutriscore2021tag" ("value");',
    )

    await connection.execute(
        'create table "product_nutriscore2023tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nutriscore2023tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_nutriscore2023tag_value_index" on "product_nutriscore2023tag" ("value");',
    )

    await connection.execute(
        'create table "product_nutriscore_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nutriscore_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_nutriscore_tag_value_index" on "product_nutriscore_tag" ("value");',
    )

    await connection.execute(
        'create table "product_packaging_materials_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_packaging_materials_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_packaging_materials_tag_value_index" on "product_packaging_materials_tag" ("value");',
    )

    await connection.execute(
        'create table "product_packaging_recycling_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_packaging_recycling_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_packaging_recycling_tag_value_index" on "product_packaging_recycling_tag" ("value");',
    )

    await connection.execute(
        'create table "product_packaging_shapes_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_packaging_shapes_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_packaging_shapes_tag_value_index" on "product_packaging_shapes_tag" ("value");',
    )

    await connection.execute(
        'create table "product_photographers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_photographers_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_photographers_tag_value_index" on "product_photographers_tag" ("value");',
    )

    await connection.execute(
        'create table "product_pnns_groups1tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_pnns_groups1tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_pnns_groups1tag_value_index" on "product_pnns_groups1tag" ("value");',
    )

    await connection.execute(
        'create table "product_pnns_groups2tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_pnns_groups2tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_pnns_groups2tag_value_index" on "product_pnns_groups2tag" ("value");',
    )

    await connection.execute(
        'create table "product_popularity_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_popularity_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_popularity_tag_value_index" on "product_popularity_tag" ("value");',
    )

    await connection.execute(
        'create table "product_purchase_places_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_purchase_places_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_purchase_places_tag_value_index" on "product_purchase_places_tag" ("value");',
    )

    await connection.execute(
        'create table "product_unknown_nutrients_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_unknown_nutrients_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_unknown_nutrients_tag_value_index" on "product_unknown_nutrients_tag" ("value");',
    )

    await connection.execute(
        'create table "product_weighers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_weighers_tag_pkey" primary key ("product_id", "value"));',
    )
    await connection.execute(
        'create index "product_weighers_tag_value_index" on "product_weighers_tag" ("value");',
    )

    await connection.execute(
        'alter table "product_categories_properites_tag" add constraint "product_categories_properites_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_checkers_tag" add constraint "product_checkers_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_cities_tag" add constraint "product_cities_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_correctors_tag" add constraint "product_correctors_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_debug_tag" add constraint "product_debug_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_food_groups_tag" add constraint "product_food_groups_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_informers_tag" add constraint "product_informers_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_c5e4a_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_latest_image_dates_tag" add constraint "product_latest_image_dates_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_nutriscore2021tag" add constraint "product_nutriscore2021tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_nutriscore2023tag" add constraint "product_nutriscore2023tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_nutriscore_tag" add constraint "product_nutriscore_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_packaging_materials_tag" add constraint "product_packaging_materials_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_packaging_recycling_tag" add constraint "product_packaging_recycling_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_packaging_shapes_tag" add constraint "product_packaging_shapes_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_photographers_tag" add constraint "product_photographers_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_pnns_groups1tag" add constraint "product_pnns_groups1tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_pnns_groups2tag" add constraint "product_pnns_groups2tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_popularity_tag" add constraint "product_popularity_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_purchase_places_tag" add constraint "product_purchase_places_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )

    await connection.execute(
        'alter table "product_weighers_tag" add constraint "product_weighers_tag_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
