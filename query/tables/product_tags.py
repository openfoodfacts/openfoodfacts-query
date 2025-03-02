tag_tables = {
    "countries_tags": "product_countries_tag",
    "nutrition_grades_tags": "product_nutrition_grades_tag",
    "nova_groups_tags": "product_nova_groups_tag",
    "ecoscore_tags": "product_ecoscore_tag",
    "brands_tags": "product_brands_tag",
    "categories_tags": "product_categories_tag",
    "labels_tags": "product_labels_tag",
    "packaging_tags": "product_packaging_tag",
    "origins_tags": "product_origins_tag",
    "manufacturing_places_tags": "product_manufacturing_places_tag",
    "emb_codes_tags": "product_emb_codes_tag",
    "ingredients_tags": "product_ingredients_tag",
    "additives_tags": "product_additives_tag",
    "vitamins_tags": "product_vitamins_tag",
    "minerals_tags": "product_minerals_tag",
    "amino_acids_tags": "product_amino_acids_tag",
    "nucleotides_tags": "product_nucleotides_tag",
    "other_nutritional_substances_tags": "product_other_nutritional_substances_tag",
    "allergens_tags": "product_allergens_tag",
    "traces_tags": "product_traces_tag",
    "misc_tags": "product_misc_tag",
    "languages_tags": "product_languages_tag",
    "states_tags": "product_states_tag",
    "data_sources_tags": "product_data_sources_tag",
    "entry_dates_tags": "product_entry_dates_tag",
    "last_edit_dates_tags": "product_last_edit_dates_tag",
    "last_check_dates_tags": "product_last_check_dates_tag",
    "teams_tags": "product_teams_tag",
    "_keywords": "product_keywords_tag",
    "codes_tags": "product_codes_tag",
    "data_quality_errors_tags": "product_data_quality_errors_tag",
    "data_quality_tags": "product_data_quality_tag",
    "editors_tags": "product_editors_tag",
    "stores_tags": "product_stores_tag",
    "ingredients_original_tags": "product_ingredients_original_tag",
    "checkers_tags": "product_checkers_tag",
    "cities_tags": "product_cities_tag",
    "correctors_tags": "product_correctors_tag",
    "debug_tags": "product_debug_tag",
    "informers_tags": "product_informers_tag",
    "ingredients_from_palm_oil_tags": "product_ingredients_from_palm_oil_tag",
    "ingredients_that_may_be_from_palm_oil_tags": "product_ingredients_that_may_be_from_palm_oil_tag",
    "last_image_dates_tags": "product_latest_image_dates_tag",
    "ingredients_n_tags": "product_ingredients_ntag",
    "nutrient_levels_tags": "product_nutrient_levels_tag",
    "periods_after_opening_tags": "product_periods_after_opening_tag",
    "photographers_tags": "product_photographers_tag",
    "pnns_groups_1_tags": "product_pnns_groups1tag",
    "pnns_groups_2_tags": "product_pnns_groups2tag",
    "purchase_places_tags": "product_purchase_places_tag",
    "unknown_nutrients_tags": "product_unknown_nutrients_tag",
    "popularity_tags": "product_popularity_tag",
    "ingredients_analysis_tags": "product_ingredients_analysis_tag",
    "data_quality_bugs_tags": "product_data_quality_bugs_tag",
    "data_quality_warnings_tags": "product_data_quality_warnings_tag",
    "categories_properties_tags": "product_categories_properites_tag",
    "food_groups_tags": "product_food_groups_tag",
    "weighers_tags": "product_weighers_tag",
    "packaging_shapes_tags": "product_packaging_shapes_tag",
    "packaging_materials_tags": "product_packaging_materials_tag",
    "packaging_recycling_tags": "product_packaging_recycling_tag",
    "nutriscore_tags": "product_nutriscore_tag",
    "nutriscore_2021_tags": "product_nutriscore2021tag",
    "nutriscore_2023_tags": "product_nutriscore2023tag"
}

async def create_tables(connection):
    for table_name in tag_tables.values():
        await connection.execute(
            f'create table {table_name} (product_id int not null, value text not null, obsolete boolean null default false, constraint {table_name}_pkey primary key (value, product_id));',
        )
        await connection.execute(
            f'create index {table_name}_product_id_index on {table_name} (product_id);'
        )
        await connection.execute(
            f'alter table {table_name} add constraint {table_name}_product_id_foreign foreign key (product_id) references product (id) on update cascade on delete cascade;',
        )


    

