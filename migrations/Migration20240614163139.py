import query.repositories.product as product

async def up(connection):
    # Changing product id from a UUID to an integer. Migration steps are as follows:
    # 1. Drop all existing primary keys that reference product_id (CASCADE removes foreign keys too)
    # 2. Drop old value index
    # 3. Rename old product id column
    # 4. Add new integer product id column
    # 5. Update new column for tags
    # 6. Make column not null
    # 7. Add back primary keys
    # 8. Add product id index
    # 9. Add back foreign keys
    # 10. Drop old column

    # 1. Drop all existing primary keys that reference product_id (CASCADE removes foreign keys too)
    await connection.execute(
        "alter table query.product_additives_tag DROP CONSTRAINT product_additives_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_allergens_tag DROP CONSTRAINT product_allergens_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_amino_acids_tag DROP CONSTRAINT product_amino_acids_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_brands_tag DROP CONSTRAINT product_brands_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_categories_properites_tag DROP CONSTRAINT product_categories_properites_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_categories_tag DROP CONSTRAINT product_categories_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_checkers_tag DROP CONSTRAINT product_checkers_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_cities_tag DROP CONSTRAINT product_cities_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_codes_tag DROP CONSTRAINT product_codes_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_correctors_tag DROP CONSTRAINT product_correctors_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_countries_tag DROP CONSTRAINT product_countries_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_data_quality_bugs_tag DROP CONSTRAINT product_data_quality_bugs_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_data_quality_errors_tag DROP CONSTRAINT product_data_quality_errors_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_data_quality_tag DROP CONSTRAINT product_data_quality_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_data_quality_warnings_tag DROP CONSTRAINT product_data_quality_warnings_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_data_sources_tag DROP CONSTRAINT product_data_sources_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_debug_tag DROP CONSTRAINT product_debug_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ecoscore_tag DROP CONSTRAINT product_ecoscore_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_editors_tag DROP CONSTRAINT product_editors_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_emb_codes_tag DROP CONSTRAINT product_emb_codes_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_entry_dates_tag DROP CONSTRAINT product_entry_dates_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_food_groups_tag DROP CONSTRAINT product_food_groups_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_informers_tag DROP CONSTRAINT product_informers_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ingredient DROP CONSTRAINT product_ingredient_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ingredients_analysis_tag DROP CONSTRAINT product_ingredients_analysis_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ingredients_from_palm_oil_tag DROP CONSTRAINT product_ingredients_from_palm_oil_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ingredients_ntag DROP CONSTRAINT product_ingredients_ntag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ingredients_original_tag DROP CONSTRAINT product_ingredients_original_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ingredients_tag DROP CONSTRAINT product_ingredients_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_ingredients_that_may_be_from_palm_oil_tag DROP CONSTRAINT product_ingredients_that_may_be_from_palm_oil_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_keywords_tag DROP CONSTRAINT product_keywords_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_labels_tag DROP CONSTRAINT product_labels_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_languages_tag DROP CONSTRAINT product_languages_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_last_check_dates_tag DROP CONSTRAINT product_last_check_dates_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_last_edit_dates_tag DROP CONSTRAINT product_last_edit_dates_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_latest_image_dates_tag DROP CONSTRAINT product_latest_image_dates_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_manufacturing_places_tag DROP CONSTRAINT product_manufacturing_places_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_minerals_tag DROP CONSTRAINT product_minerals_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_misc_tag DROP CONSTRAINT product_misc_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_nova_groups_tag DROP CONSTRAINT product_nova_groups_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_nucleotides_tag DROP CONSTRAINT product_nucleotides_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_nutrient_levels_tag DROP CONSTRAINT product_nutrient_levels_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_nutriscore_tag DROP CONSTRAINT product_nutriscore_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2021tag DROP CONSTRAINT product_nutriscore2021tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2023tag DROP CONSTRAINT product_nutriscore2023tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_nutrition_grades_tag DROP CONSTRAINT product_nutrition_grades_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_origins_tag DROP CONSTRAINT product_origins_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_other_nutritional_substances_tag DROP CONSTRAINT product_other_nutritional_substances_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_packaging_materials_tag DROP CONSTRAINT product_packaging_materials_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_packaging_recycling_tag DROP CONSTRAINT product_packaging_recycling_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_packaging_shapes_tag DROP CONSTRAINT product_packaging_shapes_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_packaging_tag DROP CONSTRAINT product_packaging_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_periods_after_opening_tag DROP CONSTRAINT product_periods_after_opening_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_photographers_tag DROP CONSTRAINT product_photographers_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups1tag DROP CONSTRAINT product_pnns_groups1tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups2tag DROP CONSTRAINT product_pnns_groups2tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_popularity_tag DROP CONSTRAINT product_popularity_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_purchase_places_tag DROP CONSTRAINT product_purchase_places_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_states_tag DROP CONSTRAINT product_states_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_stores_tag DROP CONSTRAINT product_stores_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_teams_tag DROP CONSTRAINT product_teams_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_traces_tag DROP CONSTRAINT product_traces_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_unknown_nutrients_tag DROP CONSTRAINT product_unknown_nutrients_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_vitamins_tag DROP CONSTRAINT product_vitamins_tag_pkey CASCADE;"
    )
    await connection.execute(
        "alter table query.product_weighers_tag DROP CONSTRAINT product_weighers_tag_pkey CASCADE;"
    )

    await product.drop_pkey(connection)

    # 2. Drop old value index
    await connection.execute('drop index "product_additives_tag_value_index";')
    await connection.execute('drop index "product_allergens_tag_value_index";')
    await connection.execute('drop index "product_amino_acids_tag_value_index";')
    await connection.execute('drop index "product_brands_tag_value_index";')
    await connection.execute(
        'drop index "product_categories_properites_tag_value_index";'
    )
    await connection.execute('drop index "product_categories_tag_value_index";')
    await connection.execute('drop index "product_checkers_tag_value_index";')
    await connection.execute('drop index "product_cities_tag_value_index";')
    await connection.execute('drop index "product_codes_tag_value_index";')
    await connection.execute('drop index "product_correctors_tag_value_index";')
    await connection.execute('drop index "product_countries_tag_value_index";')
    await connection.execute(
        'drop index "product_data_quality_bugs_tag_value_index";'
    )
    await connection.execute(
        'drop index "product_data_quality_errors_tag_value_index";'
    )
    await connection.execute('drop index "product_data_quality_tag_value_index";')
    await connection.execute(
        'drop index "product_data_quality_warnings_tag_value_index";'
    )
    await connection.execute('drop index "product_data_sources_tag_value_index";')
    await connection.execute('drop index "product_debug_tag_value_index";')
    await connection.execute('drop index "product_ecoscore_tag_value_index";')
    await connection.execute('drop index "product_editors_tag_value_index";')
    await connection.execute('drop index "product_emb_codes_tag_value_index";')
    await connection.execute('drop index "product_entry_dates_tag_value_index";')
    await connection.execute('drop index "product_food_groups_tag_value_index";')
    await connection.execute('drop index "product_informers_tag_value_index";')
    await connection.execute(
        'drop index "product_ingredients_analysis_tag_value_index";'
    )
    await connection.execute(
        'drop index "product_ingredients_from_palm_oil_tag_value_index";'
    )
    await connection.execute('drop index "product_ingredients_ntag_value_index";')
    await connection.execute(
        'drop index "product_ingredients_original_tag_value_index";'
    )
    await connection.execute('drop index "product_ingredients_tag_value_index";')
    await connection.execute(
        'drop index "product_ingredients_that_may_be_from_palm_oil_tag_value_index";'
    )
    await connection.execute('drop index "product_keywords_tag_value_index";')
    await connection.execute('drop index "product_labels_tag_value_index";')
    await connection.execute('drop index "product_languages_tag_value_index";')
    await connection.execute('drop index "product_last_check_dates_tag_value_index";')
    await connection.execute('drop index "product_last_edit_dates_tag_value_index";')
    await connection.execute(
        'drop index "product_latest_image_dates_tag_value_index";'
    )
    await connection.execute(
        'drop index "product_manufacturing_places_tag_value_index";'
    )
    await connection.execute('drop index "product_minerals_tag_value_index";')
    await connection.execute('drop index "product_misc_tag_value_index";')
    await connection.execute('drop index "product_nova_groups_tag_value_index";')
    await connection.execute('drop index "product_nucleotides_tag_value_index";')
    await connection.execute('drop index "product_nutrient_levels_tag_value_index";')
    await connection.execute('drop index "product_nutriscore_tag_value_index";')
    await connection.execute('drop index "product_nutriscore2021tag_value_index";')
    await connection.execute('drop index "product_nutriscore2023tag_value_index";')
    await connection.execute('drop index "product_nutrition_grades_tag_value_index";')
    await connection.execute('drop index "product_origins_tag_value_index";')
    await connection.execute(
        'drop index "product_other_nutritional_substances_tag_value_index";'
    )
    await connection.execute(
        'drop index "product_packaging_materials_tag_value_index";'
    )
    await connection.execute(
        'drop index "product_packaging_recycling_tag_value_index";'
    )
    await connection.execute('drop index "product_packaging_shapes_tag_value_index";')
    await connection.execute('drop index "product_packaging_tag_value_index";')
    await connection.execute(
        'drop index "product_periods_after_opening_tag_value_index";'
    )
    await connection.execute('drop index "product_photographers_tag_value_index";')
    await connection.execute('drop index "product_pnns_groups1tag_value_index";')
    await connection.execute('drop index "product_pnns_groups2tag_value_index";')
    await connection.execute('drop index "product_popularity_tag_value_index";')
    await connection.execute('drop index "product_purchase_places_tag_value_index";')
    await connection.execute('drop index "product_states_tag_value_index";')
    await connection.execute('drop index "product_stores_tag_value_index";')
    await connection.execute('drop index "product_teams_tag_value_index";')
    await connection.execute('drop index "product_traces_tag_value_index";')
    await connection.execute(
        'drop index "product_unknown_nutrients_tag_value_index";'
    )
    await connection.execute('drop index "product_vitamins_tag_value_index";')
    await connection.execute('drop index "product_weighers_tag_value_index";')

    # 3. Rename old product id column
    await connection.execute(
        "alter table query.product_additives_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_allergens_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_amino_acids_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_brands_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_categories_properites_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_categories_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_checkers_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_cities_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_codes_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_correctors_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_countries_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_bugs_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_errors_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_warnings_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_sources_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_debug_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ecoscore_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_editors_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_emb_codes_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_entry_dates_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_food_groups_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_informers_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredient RENAME COLUMN parent_product_id TO old_parent_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredient RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_analysis_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_from_palm_oil_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_ntag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_original_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_that_may_be_from_palm_oil_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_keywords_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_labels_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_languages_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_last_check_dates_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_last_edit_dates_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_latest_image_dates_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_manufacturing_places_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_minerals_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_misc_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nova_groups_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nucleotides_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutrient_levels_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutriscore_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2021tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2023tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutrition_grades_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_origins_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_other_nutritional_substances_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_materials_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_recycling_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_shapes_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_periods_after_opening_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_photographers_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups1tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups2tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_popularity_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_purchase_places_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_states_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_stores_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_teams_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_traces_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_unknown_nutrients_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_vitamins_tag RENAME COLUMN product_id TO old_product_id;"
    )
    await connection.execute(
        "alter table query.product_weighers_tag RENAME COLUMN product_id TO old_product_id;"
    )

    # 4. Add new integer product id column
    await connection.execute(
        "alter table query.product_additives_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_allergens_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_amino_acids_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_brands_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_categories_properites_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_categories_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_checkers_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_cities_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_codes_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_correctors_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_countries_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_bugs_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_errors_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_warnings_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_data_sources_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_debug_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ecoscore_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_editors_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_emb_codes_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_entry_dates_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_food_groups_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_informers_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredient ADD COLUMN parent_product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredient ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_analysis_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_from_palm_oil_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_ntag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_original_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_that_may_be_from_palm_oil_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_keywords_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_labels_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_languages_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_last_check_dates_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_last_edit_dates_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_latest_image_dates_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_manufacturing_places_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_minerals_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_misc_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_nova_groups_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_nucleotides_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_nutrient_levels_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_nutriscore_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2021tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2023tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_nutrition_grades_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_origins_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_other_nutritional_substances_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_materials_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_recycling_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_shapes_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_periods_after_opening_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_photographers_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups1tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups2tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_popularity_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_purchase_places_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_states_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_stores_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_teams_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_traces_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_unknown_nutrients_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_vitamins_tag ADD COLUMN product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_weighers_tag ADD COLUMN product_id int NULL;"
    )

    # 5. Update new column for tags
    await connection.execute(
        "update query.product_additives_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_allergens_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_amino_acids_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_brands_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_categories_properites_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_categories_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_checkers_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_cities_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_codes_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_correctors_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_countries_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_data_quality_bugs_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_data_quality_errors_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_data_quality_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_data_quality_warnings_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_data_sources_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_debug_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ecoscore_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_editors_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_emb_codes_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_entry_dates_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_food_groups_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_informers_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredient set parent_product_id = product.id from query.product WHERE old_id = old_parent_product_id AND parent_product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredient set product_id = product.id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredients_analysis_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredients_from_palm_oil_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredients_ntag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredients_original_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredients_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredients_that_may_be_from_palm_oil_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_keywords_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_labels_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_languages_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_last_check_dates_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_last_edit_dates_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_latest_image_dates_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_manufacturing_places_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_minerals_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_misc_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_nova_groups_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_nucleotides_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_nutrient_levels_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_nutriscore_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_nutriscore2021tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_nutriscore2023tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_nutrition_grades_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_origins_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_other_nutritional_substances_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_packaging_materials_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_packaging_recycling_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_packaging_shapes_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_packaging_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_periods_after_opening_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_photographers_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_pnns_groups1tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_pnns_groups2tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_popularity_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_purchase_places_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_states_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_stores_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_teams_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_traces_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_unknown_nutrients_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_vitamins_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_weighers_tag set product_id = id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )

    # 6. Make column not null
    await connection.execute(
        "alter table query.product_additives_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_allergens_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_amino_acids_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_brands_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_categories_properites_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_categories_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_checkers_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_cities_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_codes_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_correctors_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_countries_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_bugs_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_errors_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_data_quality_warnings_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_data_sources_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_debug_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ecoscore_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_editors_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_emb_codes_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_entry_dates_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_food_groups_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_informers_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredient alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_analysis_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_from_palm_oil_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_ntag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_original_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredients_that_may_be_from_palm_oil_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_keywords_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_labels_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_languages_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_last_check_dates_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_last_edit_dates_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_latest_image_dates_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_manufacturing_places_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_minerals_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_misc_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_nova_groups_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_nucleotides_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_nutrient_levels_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_nutriscore_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2021tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2023tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_nutrition_grades_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_origins_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_other_nutritional_substances_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_materials_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_recycling_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_shapes_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_packaging_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_periods_after_opening_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_photographers_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups1tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups2tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_popularity_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_purchase_places_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_states_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_stores_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_teams_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_traces_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_unknown_nutrients_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_vitamins_tag alter column product_id SET NOT NULL;"
    )
    await connection.execute(
        "alter table query.product_weighers_tag alter column product_id SET NOT NULL;"
    )

    # 7. Add back primary keys
    await connection.execute(
        'alter table "product_additives_tag" add constraint "product_additives_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_allergens_tag" add constraint "product_allergens_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_amino_acids_tag" add constraint "product_amino_acids_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_brands_tag" add constraint "product_brands_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_categories_properites_tag" add constraint "product_categories_properites_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_categories_tag" add constraint "product_categories_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_checkers_tag" add constraint "product_checkers_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_cities_tag" add constraint "product_cities_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_codes_tag" add constraint "product_codes_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_correctors_tag" add constraint "product_correctors_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_countries_tag" add constraint "product_countries_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_data_quality_tag" add constraint "product_data_quality_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_data_sources_tag" add constraint "product_data_sources_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_debug_tag" add constraint "product_debug_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_ecoscore_tag" add constraint "product_ecoscore_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_editors_tag" add constraint "product_editors_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_emb_codes_tag" add constraint "product_emb_codes_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_entry_dates_tag" add constraint "product_entry_dates_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_food_groups_tag" add constraint "product_food_groups_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_informers_tag" add constraint "product_informers_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        "alter table query.product_ingredient ADD CONSTRAINT product_ingredient_pkey PRIMARY KEY (product_id,sequence);"
    )
    await connection.execute(
        'alter table "product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_ingredients_ntag" add constraint "product_ingredients_ntag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_ingredients_original_tag" add constraint "product_ingredients_original_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_ingredients_tag" add constraint "product_ingredients_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_keywords_tag" add constraint "product_keywords_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_labels_tag" add constraint "product_labels_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_languages_tag" add constraint "product_languages_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_last_check_dates_tag" add constraint "product_last_check_dates_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_latest_image_dates_tag" add constraint "product_latest_image_dates_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_minerals_tag" add constraint "product_minerals_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_misc_tag" add constraint "product_misc_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_nova_groups_tag" add constraint "product_nova_groups_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_nucleotides_tag" add constraint "product_nucleotides_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_nutriscore_tag" add constraint "product_nutriscore_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_nutriscore2021tag" add constraint "product_nutriscore2021tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_nutriscore2023tag" add constraint "product_nutriscore2023tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_origins_tag" add constraint "product_origins_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_other_nutritional_substances_tag" add constraint "product_other_nutritional_substances_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_packaging_materials_tag" add constraint "product_packaging_materials_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_packaging_recycling_tag" add constraint "product_packaging_recycling_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_packaging_shapes_tag" add constraint "product_packaging_shapes_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_packaging_tag" add constraint "product_packaging_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_periods_after_opening_tag" add constraint "product_periods_after_opening_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_photographers_tag" add constraint "product_photographers_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_pnns_groups1tag" add constraint "product_pnns_groups1tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_pnns_groups2tag" add constraint "product_pnns_groups2tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_popularity_tag" add constraint "product_popularity_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_purchase_places_tag" add constraint "product_purchase_places_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_states_tag" add constraint "product_states_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_stores_tag" add constraint "product_stores_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_teams_tag" add constraint "product_teams_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_traces_tag" add constraint "product_traces_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_vitamins_tag" add constraint "product_vitamins_tag_pkey" primary key ("value", "product_id");'
    )
    await connection.execute(
        'alter table "product_weighers_tag" add constraint "product_weighers_tag_pkey" primary key ("value", "product_id");'
    )

    # 8. Add product id index
    await connection.execute(
        'create index "product_additives_tag_product_id_index" on "product_additives_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_allergens_tag_product_id_index" on "product_allergens_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_amino_acids_tag_product_id_index" on "product_amino_acids_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_brands_tag_product_id_index" on "product_brands_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_categories_properites_tag_product_id_index" on "product_categories_properites_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_categories_tag_product_id_index" on "product_categories_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_checkers_tag_product_id_index" on "product_checkers_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_cities_tag_product_id_index" on "product_cities_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_codes_tag_product_id_index" on "product_codes_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_correctors_tag_product_id_index" on "product_correctors_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_countries_tag_product_id_index" on "product_countries_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_data_quality_bugs_tag_product_id_index" on "product_data_quality_bugs_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_data_quality_errors_tag_product_id_index" on "product_data_quality_errors_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_data_quality_tag_product_id_index" on "product_data_quality_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_data_quality_warnings_tag_product_id_index" on "product_data_quality_warnings_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_data_sources_tag_product_id_index" on "product_data_sources_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_debug_tag_product_id_index" on "product_debug_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_ecoscore_tag_product_id_index" on "product_ecoscore_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_editors_tag_product_id_index" on "product_editors_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_emb_codes_tag_product_id_index" on "product_emb_codes_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_entry_dates_tag_product_id_index" on "product_entry_dates_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_food_groups_tag_product_id_index" on "product_food_groups_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_informers_tag_product_id_index" on "product_informers_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_ingredients_analysis_tag_product_id_index" on "product_ingredients_analysis_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_ingredients_from_palm_oil_tag_product_id_index" on "product_ingredients_from_palm_oil_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_ingredients_ntag_product_id_index" on "product_ingredients_ntag" ("product_id");'
    )
    await connection.execute(
        'create index "product_ingredients_original_tag_product_id_index" on "product_ingredients_original_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_ingredients_tag_product_id_index" on "product_ingredients_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_ingredients_that_may_be_from_palm_oil_tag_p_d0162_index" on "product_ingredients_that_may_be_from_palm_oil_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_keywords_tag_product_id_index" on "product_keywords_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_labels_tag_product_id_index" on "product_labels_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_languages_tag_product_id_index" on "product_languages_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_last_check_dates_tag_product_id_index" on "product_last_check_dates_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_last_edit_dates_tag_product_id_index" on "product_last_edit_dates_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_latest_image_dates_tag_product_id_index" on "product_latest_image_dates_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_manufacturing_places_tag_product_id_index" on "product_manufacturing_places_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_minerals_tag_product_id_index" on "product_minerals_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_misc_tag_product_id_index" on "product_misc_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_nova_groups_tag_product_id_index" on "product_nova_groups_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_nucleotides_tag_product_id_index" on "product_nucleotides_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_nutrient_levels_tag_product_id_index" on "product_nutrient_levels_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_nutriscore_tag_product_id_index" on "product_nutriscore_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_nutriscore2021tag_product_id_index" on "product_nutriscore2021tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_nutriscore2023tag_product_id_index" on "product_nutriscore2023tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_nutrition_grades_tag_product_id_index" on "product_nutrition_grades_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_origins_tag_product_id_index" on "product_origins_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_other_nutritional_substances_tag_product_id_index" on "product_other_nutritional_substances_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_packaging_materials_tag_product_id_index" on "product_packaging_materials_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_packaging_recycling_tag_product_id_index" on "product_packaging_recycling_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_packaging_shapes_tag_product_id_index" on "product_packaging_shapes_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_packaging_tag_product_id_index" on "product_packaging_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_periods_after_opening_tag_product_id_index" on "product_periods_after_opening_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_photographers_tag_product_id_index" on "product_photographers_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_pnns_groups1tag_product_id_index" on "product_pnns_groups1tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_pnns_groups2tag_product_id_index" on "product_pnns_groups2tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_popularity_tag_product_id_index" on "product_popularity_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_purchase_places_tag_product_id_index" on "product_purchase_places_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_states_tag_product_id_index" on "product_states_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_stores_tag_product_id_index" on "product_stores_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_teams_tag_product_id_index" on "product_teams_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_traces_tag_product_id_index" on "product_traces_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_unknown_nutrients_tag_product_id_index" on "product_unknown_nutrients_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_vitamins_tag_product_id_index" on "product_vitamins_tag" ("product_id");'
    )
    await connection.execute(
        'create index "product_weighers_tag_product_id_index" on "product_weighers_tag" ("product_id");'
    )

    # 9. Add back foreign keys
    await connection.execute(
        'alter table query.product_additives_tag add constraint product_additives_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_allergens_tag add constraint product_allergens_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_amino_acids_tag add constraint product_amino_acids_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_brands_tag add constraint product_brands_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_categories_properites_tag add constraint product_categories_properites_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_categories_tag add constraint product_categories_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_checkers_tag add constraint product_checkers_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_cities_tag add constraint product_cities_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_codes_tag add constraint product_codes_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_correctors_tag add constraint product_correctors_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_countries_tag add constraint product_countries_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_data_quality_bugs_tag add constraint product_data_quality_bugs_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_data_quality_errors_tag add constraint product_data_quality_errors_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_data_quality_tag add constraint product_data_quality_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_data_quality_warnings_tag add constraint product_data_quality_warnings_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_data_sources_tag add constraint product_data_sources_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_debug_tag add constraint product_debug_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ecoscore_tag add constraint product_ecoscore_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_editors_tag add constraint product_editors_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_emb_codes_tag add constraint product_emb_codes_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_entry_dates_tag add constraint product_entry_dates_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_food_groups_tag add constraint product_food_groups_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_informers_tag add constraint product_informers_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ingredient add constraint product_ingredient_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ingredients_analysis_tag add constraint product_ingredients_analysis_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ingredients_from_palm_oil_tag add constraint product_ingredients_from_palm_oil_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ingredients_ntag add constraint product_ingredients_ntag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ingredients_original_tag add constraint product_ingredients_original_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ingredients_tag add constraint product_ingredients_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_ingredients_that_may_be_from_palm_oil_tag add constraint product_ingredients_that_may_be_from_palm_oil_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_keywords_tag add constraint product_keywords_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_labels_tag add constraint product_labels_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_languages_tag add constraint product_languages_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_last_check_dates_tag add constraint product_last_check_dates_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_last_edit_dates_tag add constraint product_last_edit_dates_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_latest_image_dates_tag add constraint product_latest_image_dates_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_manufacturing_places_tag add constraint product_manufacturing_places_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_minerals_tag add constraint product_minerals_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_misc_tag add constraint product_misc_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_nova_groups_tag add constraint product_nova_groups_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_nucleotides_tag add constraint product_nucleotides_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_nutrient_levels_tag add constraint product_nutrient_levels_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_nutriscore_tag add constraint product_nutriscore_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_nutriscore2021tag add constraint product_nutriscore2021tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_nutriscore2023tag add constraint product_nutriscore2023tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_nutrition_grades_tag add constraint product_nutrition_grades_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_origins_tag add constraint product_origins_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_other_nutritional_substances_tag add constraint product_other_nutritional_substances_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_packaging_materials_tag add constraint product_packaging_materials_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_packaging_recycling_tag add constraint product_packaging_recycling_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_packaging_shapes_tag add constraint product_packaging_shapes_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_packaging_tag add constraint product_packaging_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_periods_after_opening_tag add constraint product_periods_after_opening_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_photographers_tag add constraint product_photographers_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_pnns_groups1tag add constraint product_pnns_groups1tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_pnns_groups2tag add constraint product_pnns_groups2tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_popularity_tag add constraint product_popularity_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_purchase_places_tag add constraint product_purchase_places_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_states_tag add constraint product_states_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_stores_tag add constraint product_stores_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_teams_tag add constraint product_teams_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_traces_tag add constraint product_traces_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_unknown_nutrients_tag add constraint product_unknown_nutrients_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_vitamins_tag add constraint product_vitamins_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )
    await connection.execute(
        'alter table query.product_weighers_tag add constraint product_weighers_tag_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )

    # 10. Drop old column
    await connection.execute(
        "alter table query.product_additives_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_allergens_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_amino_acids_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_brands_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_categories_properites_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_categories_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_checkers_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_cities_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_codes_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_correctors_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_countries_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_bugs_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_errors_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_quality_warnings_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_data_sources_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_debug_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ecoscore_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_editors_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_emb_codes_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_entry_dates_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_food_groups_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_informers_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredient drop column old_parent_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredient drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_analysis_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_from_palm_oil_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_ntag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_original_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredients_that_may_be_from_palm_oil_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_keywords_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_labels_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_languages_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_last_check_dates_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_last_edit_dates_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_latest_image_dates_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_manufacturing_places_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_minerals_tag drop column old_product_id;"
    )
    await connection.execute("alter table query.product_misc_tag drop column old_product_id;")
    await connection.execute(
        "alter table query.product_nova_groups_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nucleotides_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutrient_levels_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutriscore_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2021tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutriscore2023tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_nutrition_grades_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_origins_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_other_nutritional_substances_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_materials_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_recycling_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_shapes_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_packaging_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_periods_after_opening_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_photographers_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups1tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_pnns_groups2tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_popularity_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_purchase_places_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_states_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_stores_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_teams_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_traces_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_unknown_nutrients_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_vitamins_tag drop column old_product_id;"
    )
    await connection.execute(
        "alter table query.product_weighers_tag drop column old_product_id;"
    )

    await product.drop_old_id(connection)

    await connection.execute(
        'create index "product_ingredient_parent_product_id_parent_sequence_index" on "product_ingredient" ("parent_product_id", "parent_sequence");'
    )
