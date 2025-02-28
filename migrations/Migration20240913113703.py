async def up(connection):
    await connection.execute(
        'alter table "product" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_additives_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_additives_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_allergens_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_allergens_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_amino_acids_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_amino_acids_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_brands_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_brands_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_categories_properites_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_categories_properites_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_categories_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_categories_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_checkers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_checkers_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_cities_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_cities_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_codes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_codes_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_correctors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_correctors_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_countries_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_countries_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_data_quality_bugs_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_data_quality_bugs_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_data_quality_errors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_data_quality_errors_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_data_quality_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_data_quality_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_data_quality_warnings_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_data_quality_warnings_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_data_sources_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_data_sources_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_debug_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_debug_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ecoscore_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ecoscore_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_editors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_editors_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_emb_codes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_emb_codes_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_entry_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_entry_dates_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_food_groups_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_food_groups_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_informers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_informers_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ingredient" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredient" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ingredients_analysis_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredients_analysis_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ingredients_from_palm_oil_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredients_from_palm_oil_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ingredients_ntag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredients_ntag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ingredients_original_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredients_original_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ingredients_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredients_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_ingredients_that_may_be_from_palm_oil_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_ingredients_that_may_be_from_palm_oil_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_keywords_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_keywords_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_labels_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_labels_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_languages_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_languages_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_last_check_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_last_check_dates_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_last_edit_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_last_edit_dates_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_latest_image_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_latest_image_dates_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_manufacturing_places_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_manufacturing_places_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_minerals_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_minerals_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_misc_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_misc_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_nova_groups_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_nova_groups_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_nucleotides_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_nucleotides_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_nutrient_levels_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_nutrient_levels_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_nutriscore2021tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_nutriscore2021tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_nutriscore2023tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_nutriscore2023tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_nutriscore_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_nutriscore_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_nutrition_grades_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_nutrition_grades_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_origins_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_origins_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_other_nutritional_substances_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_other_nutritional_substances_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_packaging_materials_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_packaging_materials_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_packaging_recycling_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_packaging_recycling_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_packaging_shapes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_packaging_shapes_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_packaging_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_packaging_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_periods_after_opening_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_periods_after_opening_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_photographers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_photographers_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_pnns_groups1tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_pnns_groups1tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_pnns_groups2tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_pnns_groups2tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_popularity_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_popularity_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_purchase_places_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_purchase_places_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_states_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_states_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_stores_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_stores_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_teams_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_teams_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_traces_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_traces_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_unknown_nutrients_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_unknown_nutrients_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_vitamins_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_vitamins_tag" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product_weighers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product_weighers_tag" alter column "obsolete" drop not null;'
    )
