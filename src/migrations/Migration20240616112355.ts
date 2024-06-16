import { Migration } from '@mikro-orm/migrations';

export class Migration20240616112355 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."product_additives_tag" drop constraint "product_additives_tag_pkey";');
    this.addSql('create index "product_additives_tag_value_index" on "query"."product_additives_tag" ("value");');
    this.addSql('alter table "query"."product_additives_tag" add constraint "product_additives_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_allergens_tag" drop constraint "product_allergens_tag_pkey";');
    this.addSql('create index "product_allergens_tag_value_index" on "query"."product_allergens_tag" ("value");');
    this.addSql('alter table "query"."product_allergens_tag" add constraint "product_allergens_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_amino_acids_tag" drop constraint "product_amino_acids_tag_pkey";');
    this.addSql('create index "product_amino_acids_tag_value_index" on "query"."product_amino_acids_tag" ("value");');
    this.addSql('alter table "query"."product_amino_acids_tag" add constraint "product_amino_acids_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_brands_tag" drop constraint "product_brands_tag_pkey";');
    this.addSql('create index "product_brands_tag_value_index" on "query"."product_brands_tag" ("value");');
    this.addSql('alter table "query"."product_brands_tag" add constraint "product_brands_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_categories_properites_tag" drop constraint "product_categories_properites_tag_pkey";');
    this.addSql('create index "product_categories_properites_tag_value_index" on "query"."product_categories_properites_tag" ("value");');
    this.addSql('alter table "query"."product_categories_properites_tag" add constraint "product_categories_properites_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_categories_tag" drop constraint "product_categories_tag_pkey";');
    this.addSql('create index "product_categories_tag_value_index" on "query"."product_categories_tag" ("value");');
    this.addSql('alter table "query"."product_categories_tag" add constraint "product_categories_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_checkers_tag" drop constraint "product_checkers_tag_pkey";');
    this.addSql('create index "product_checkers_tag_value_index" on "query"."product_checkers_tag" ("value");');
    this.addSql('alter table "query"."product_checkers_tag" add constraint "product_checkers_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_cities_tag" drop constraint "product_cities_tag_pkey";');
    this.addSql('create index "product_cities_tag_value_index" on "query"."product_cities_tag" ("value");');
    this.addSql('alter table "query"."product_cities_tag" add constraint "product_cities_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_codes_tag" drop constraint "product_codes_tag_pkey";');
    this.addSql('create index "product_codes_tag_value_index" on "query"."product_codes_tag" ("value");');
    this.addSql('alter table "query"."product_codes_tag" add constraint "product_codes_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_correctors_tag" drop constraint "product_correctors_tag_pkey";');
    this.addSql('create index "product_correctors_tag_value_index" on "query"."product_correctors_tag" ("value");');
    this.addSql('alter table "query"."product_correctors_tag" add constraint "product_correctors_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_countries_tag" drop constraint "product_countries_tag_pkey";');
    this.addSql('create index "product_countries_tag_value_index" on "query"."product_countries_tag" ("value");');
    this.addSql('alter table "query"."product_countries_tag" add constraint "product_countries_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_data_quality_bugs_tag" drop constraint "product_data_quality_bugs_tag_pkey";');
    this.addSql('create index "product_data_quality_bugs_tag_value_index" on "query"."product_data_quality_bugs_tag" ("value");');
    this.addSql('alter table "query"."product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_data_quality_errors_tag" drop constraint "product_data_quality_errors_tag_pkey";');
    this.addSql('create index "product_data_quality_errors_tag_value_index" on "query"."product_data_quality_errors_tag" ("value");');
    this.addSql('alter table "query"."product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_data_quality_tag" drop constraint "product_data_quality_tag_pkey";');
    this.addSql('create index "product_data_quality_tag_value_index" on "query"."product_data_quality_tag" ("value");');
    this.addSql('alter table "query"."product_data_quality_tag" add constraint "product_data_quality_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_data_quality_warnings_tag" drop constraint "product_data_quality_warnings_tag_pkey";');
    this.addSql('create index "product_data_quality_warnings_tag_value_index" on "query"."product_data_quality_warnings_tag" ("value");');
    this.addSql('alter table "query"."product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_data_sources_tag" drop constraint "product_data_sources_tag_pkey";');
    this.addSql('create index "product_data_sources_tag_value_index" on "query"."product_data_sources_tag" ("value");');
    this.addSql('alter table "query"."product_data_sources_tag" add constraint "product_data_sources_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_debug_tag" drop constraint "product_debug_tag_pkey";');
    this.addSql('create index "product_debug_tag_value_index" on "query"."product_debug_tag" ("value");');
    this.addSql('alter table "query"."product_debug_tag" add constraint "product_debug_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_ecoscore_tag" drop constraint "product_ecoscore_tag_pkey";');
    this.addSql('create index "product_ecoscore_tag_value_index" on "query"."product_ecoscore_tag" ("value");');
    this.addSql('alter table "query"."product_ecoscore_tag" add constraint "product_ecoscore_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_editors_tag" drop constraint "product_editors_tag_pkey";');
    this.addSql('create index "product_editors_tag_value_index" on "query"."product_editors_tag" ("value");');
    this.addSql('alter table "query"."product_editors_tag" add constraint "product_editors_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_emb_codes_tag" drop constraint "product_emb_codes_tag_pkey";');
    this.addSql('create index "product_emb_codes_tag_value_index" on "query"."product_emb_codes_tag" ("value");');
    this.addSql('alter table "query"."product_emb_codes_tag" add constraint "product_emb_codes_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_entry_dates_tag" drop constraint "product_entry_dates_tag_pkey";');
    this.addSql('create index "product_entry_dates_tag_value_index" on "query"."product_entry_dates_tag" ("value");');
    this.addSql('alter table "query"."product_entry_dates_tag" add constraint "product_entry_dates_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_food_groups_tag" drop constraint "product_food_groups_tag_pkey";');
    this.addSql('create index "product_food_groups_tag_value_index" on "query"."product_food_groups_tag" ("value");');
    this.addSql('alter table "query"."product_food_groups_tag" add constraint "product_food_groups_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_informers_tag" drop constraint "product_informers_tag_pkey";');
    this.addSql('create index "product_informers_tag_value_index" on "query"."product_informers_tag" ("value");');
    this.addSql('alter table "query"."product_informers_tag" add constraint "product_informers_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_ingredients_analysis_tag" drop constraint "product_ingredients_analysis_tag_pkey";');
    this.addSql('create index "product_ingredients_analysis_tag_value_index" on "query"."product_ingredients_analysis_tag" ("value");');
    this.addSql('alter table "query"."product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" drop constraint "product_ingredients_from_palm_oil_tag_pkey";');
    this.addSql('create index "product_ingredients_from_palm_oil_tag_value_index" on "query"."product_ingredients_from_palm_oil_tag" ("value");');
    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_ingredients_ntag" drop constraint "product_ingredients_ntag_pkey";');
    this.addSql('create index "product_ingredients_ntag_value_index" on "query"."product_ingredients_ntag" ("value");');
    this.addSql('alter table "query"."product_ingredients_ntag" add constraint "product_ingredients_ntag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_ingredients_original_tag" drop constraint "product_ingredients_original_tag_pkey";');
    this.addSql('create index "product_ingredients_original_tag_value_index" on "query"."product_ingredients_original_tag" ("value");');
    this.addSql('alter table "query"."product_ingredients_original_tag" add constraint "product_ingredients_original_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_ingredients_tag" drop constraint "product_ingredients_tag_pkey";');
    this.addSql('create index "product_ingredients_tag_value_index" on "query"."product_ingredients_tag" ("value");');
    this.addSql('alter table "query"."product_ingredients_tag" add constraint "product_ingredients_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" drop constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey";');
    this.addSql('create index "product_ingredients_that_may_be_from_palm_oil_tag_value_index" on "query"."product_ingredients_that_may_be_from_palm_oil_tag" ("value");');
    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_keywords_tag" drop constraint "product_keywords_tag_pkey";');
    this.addSql('create index "product_keywords_tag_value_index" on "query"."product_keywords_tag" ("value");');
    this.addSql('alter table "query"."product_keywords_tag" add constraint "product_keywords_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_labels_tag" drop constraint "product_labels_tag_pkey";');
    this.addSql('create index "product_labels_tag_value_index" on "query"."product_labels_tag" ("value");');
    this.addSql('alter table "query"."product_labels_tag" add constraint "product_labels_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_languages_tag" drop constraint "product_languages_tag_pkey";');
    this.addSql('create index "product_languages_tag_value_index" on "query"."product_languages_tag" ("value");');
    this.addSql('alter table "query"."product_languages_tag" add constraint "product_languages_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_last_check_dates_tag" drop constraint "product_last_check_dates_tag_pkey";');
    this.addSql('create index "product_last_check_dates_tag_value_index" on "query"."product_last_check_dates_tag" ("value");');
    this.addSql('alter table "query"."product_last_check_dates_tag" add constraint "product_last_check_dates_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_last_edit_dates_tag" drop constraint "product_last_edit_dates_tag_pkey";');
    this.addSql('create index "product_last_edit_dates_tag_value_index" on "query"."product_last_edit_dates_tag" ("value");');
    this.addSql('alter table "query"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_latest_image_dates_tag" drop constraint "product_latest_image_dates_tag_pkey";');
    this.addSql('create index "product_latest_image_dates_tag_value_index" on "query"."product_latest_image_dates_tag" ("value");');
    this.addSql('alter table "query"."product_latest_image_dates_tag" add constraint "product_latest_image_dates_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_manufacturing_places_tag" drop constraint "product_manufacturing_places_tag_pkey";');
    this.addSql('create index "product_manufacturing_places_tag_value_index" on "query"."product_manufacturing_places_tag" ("value");');
    this.addSql('alter table "query"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_minerals_tag" drop constraint "product_minerals_tag_pkey";');
    this.addSql('create index "product_minerals_tag_value_index" on "query"."product_minerals_tag" ("value");');
    this.addSql('alter table "query"."product_minerals_tag" add constraint "product_minerals_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_misc_tag" drop constraint "product_misc_tag_pkey";');
    this.addSql('create index "product_misc_tag_value_index" on "query"."product_misc_tag" ("value");');
    this.addSql('alter table "query"."product_misc_tag" add constraint "product_misc_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_nova_groups_tag" drop constraint "product_nova_groups_tag_pkey";');
    this.addSql('create index "product_nova_groups_tag_value_index" on "query"."product_nova_groups_tag" ("value");');
    this.addSql('alter table "query"."product_nova_groups_tag" add constraint "product_nova_groups_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_nucleotides_tag" drop constraint "product_nucleotides_tag_pkey";');
    this.addSql('create index "product_nucleotides_tag_value_index" on "query"."product_nucleotides_tag" ("value");');
    this.addSql('alter table "query"."product_nucleotides_tag" add constraint "product_nucleotides_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_nutrient_levels_tag" drop constraint "product_nutrient_levels_tag_pkey";');
    this.addSql('create index "product_nutrient_levels_tag_value_index" on "query"."product_nutrient_levels_tag" ("value");');
    this.addSql('alter table "query"."product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_nutriscore2021tag" drop constraint "product_nutriscore2021tag_pkey";');
    this.addSql('create index "product_nutriscore2021tag_value_index" on "query"."product_nutriscore2021tag" ("value");');
    this.addSql('alter table "query"."product_nutriscore2021tag" add constraint "product_nutriscore2021tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_nutriscore2023tag" drop constraint "product_nutriscore2023tag_pkey";');
    this.addSql('create index "product_nutriscore2023tag_value_index" on "query"."product_nutriscore2023tag" ("value");');
    this.addSql('alter table "query"."product_nutriscore2023tag" add constraint "product_nutriscore2023tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_nutriscore_tag" drop constraint "product_nutriscore_tag_pkey";');
    this.addSql('create index "product_nutriscore_tag_value_index" on "query"."product_nutriscore_tag" ("value");');
    this.addSql('alter table "query"."product_nutriscore_tag" add constraint "product_nutriscore_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_nutrition_grades_tag" drop constraint "product_nutrition_grades_tag_pkey";');
    this.addSql('create index "product_nutrition_grades_tag_value_index" on "query"."product_nutrition_grades_tag" ("value");');
    this.addSql('alter table "query"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_origins_tag" drop constraint "product_origins_tag_pkey";');
    this.addSql('create index "product_origins_tag_value_index" on "query"."product_origins_tag" ("value");');
    this.addSql('alter table "query"."product_origins_tag" add constraint "product_origins_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_other_nutritional_substances_tag" drop constraint "product_other_nutritional_substances_tag_pkey";');
    this.addSql('create index "product_other_nutritional_substances_tag_value_index" on "query"."product_other_nutritional_substances_tag" ("value");');
    this.addSql('alter table "query"."product_other_nutritional_substances_tag" add constraint "product_other_nutritional_substances_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_packaging_materials_tag" drop constraint "product_packaging_materials_tag_pkey";');
    this.addSql('create index "product_packaging_materials_tag_value_index" on "query"."product_packaging_materials_tag" ("value");');
    this.addSql('alter table "query"."product_packaging_materials_tag" add constraint "product_packaging_materials_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_packaging_recycling_tag" drop constraint "product_packaging_recycling_tag_pkey";');
    this.addSql('create index "product_packaging_recycling_tag_value_index" on "query"."product_packaging_recycling_tag" ("value");');
    this.addSql('alter table "query"."product_packaging_recycling_tag" add constraint "product_packaging_recycling_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_packaging_shapes_tag" drop constraint "product_packaging_shapes_tag_pkey";');
    this.addSql('create index "product_packaging_shapes_tag_value_index" on "query"."product_packaging_shapes_tag" ("value");');
    this.addSql('alter table "query"."product_packaging_shapes_tag" add constraint "product_packaging_shapes_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_packaging_tag" drop constraint "product_packaging_tag_pkey";');
    this.addSql('create index "product_packaging_tag_value_index" on "query"."product_packaging_tag" ("value");');
    this.addSql('alter table "query"."product_packaging_tag" add constraint "product_packaging_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_periods_after_opening_tag" drop constraint "product_periods_after_opening_tag_pkey";');
    this.addSql('create index "product_periods_after_opening_tag_value_index" on "query"."product_periods_after_opening_tag" ("value");');
    this.addSql('alter table "query"."product_periods_after_opening_tag" add constraint "product_periods_after_opening_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_photographers_tag" drop constraint "product_photographers_tag_pkey";');
    this.addSql('create index "product_photographers_tag_value_index" on "query"."product_photographers_tag" ("value");');
    this.addSql('alter table "query"."product_photographers_tag" add constraint "product_photographers_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_pnns_groups1tag" drop constraint "product_pnns_groups1tag_pkey";');
    this.addSql('create index "product_pnns_groups1tag_value_index" on "query"."product_pnns_groups1tag" ("value");');
    this.addSql('alter table "query"."product_pnns_groups1tag" add constraint "product_pnns_groups1tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_pnns_groups2tag" drop constraint "product_pnns_groups2tag_pkey";');
    this.addSql('create index "product_pnns_groups2tag_value_index" on "query"."product_pnns_groups2tag" ("value");');
    this.addSql('alter table "query"."product_pnns_groups2tag" add constraint "product_pnns_groups2tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_popularity_tag" drop constraint "product_popularity_tag_pkey";');
    this.addSql('create index "product_popularity_tag_value_index" on "query"."product_popularity_tag" ("value");');
    this.addSql('alter table "query"."product_popularity_tag" add constraint "product_popularity_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_purchase_places_tag" drop constraint "product_purchase_places_tag_pkey";');
    this.addSql('create index "product_purchase_places_tag_value_index" on "query"."product_purchase_places_tag" ("value");');
    this.addSql('alter table "query"."product_purchase_places_tag" add constraint "product_purchase_places_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_states_tag" drop constraint "product_states_tag_pkey";');
    this.addSql('create index "product_states_tag_value_index" on "query"."product_states_tag" ("value");');
    this.addSql('alter table "query"."product_states_tag" add constraint "product_states_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_stores_tag" drop constraint "product_stores_tag_pkey";');
    this.addSql('create index "product_stores_tag_value_index" on "query"."product_stores_tag" ("value");');
    this.addSql('alter table "query"."product_stores_tag" add constraint "product_stores_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_teams_tag" drop constraint "product_teams_tag_pkey";');
    this.addSql('create index "product_teams_tag_value_index" on "query"."product_teams_tag" ("value");');
    this.addSql('alter table "query"."product_teams_tag" add constraint "product_teams_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_traces_tag" drop constraint "product_traces_tag_pkey";');
    this.addSql('create index "product_traces_tag_value_index" on "query"."product_traces_tag" ("value");');
    this.addSql('alter table "query"."product_traces_tag" add constraint "product_traces_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_unknown_nutrients_tag" drop constraint "product_unknown_nutrients_tag_pkey";');
    this.addSql('create index "product_unknown_nutrients_tag_value_index" on "query"."product_unknown_nutrients_tag" ("value");');
    this.addSql('alter table "query"."product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_vitamins_tag" drop constraint "product_vitamins_tag_pkey";');
    this.addSql('create index "product_vitamins_tag_value_index" on "query"."product_vitamins_tag" ("value");');
    this.addSql('alter table "query"."product_vitamins_tag" add constraint "product_vitamins_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "query"."product_weighers_tag" drop constraint "product_weighers_tag_pkey";');
    this.addSql('create index "product_weighers_tag_value_index" on "query"."product_weighers_tag" ("value");');
    this.addSql('alter table "query"."product_weighers_tag" add constraint "product_weighers_tag_pkey" primary key ("product_id", "value");');
  }

  async down(): Promise<void> {
    this.addSql('drop index "query"."product_additives_tag_value_index";');
    this.addSql('alter table "query"."product_additives_tag" drop constraint "product_additives_tag_pkey";');
    this.addSql('alter table "query"."product_additives_tag" add constraint "product_additives_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_allergens_tag_value_index";');
    this.addSql('alter table "query"."product_allergens_tag" drop constraint "product_allergens_tag_pkey";');
    this.addSql('alter table "query"."product_allergens_tag" add constraint "product_allergens_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_amino_acids_tag_value_index";');
    this.addSql('alter table "query"."product_amino_acids_tag" drop constraint "product_amino_acids_tag_pkey";');
    this.addSql('alter table "query"."product_amino_acids_tag" add constraint "product_amino_acids_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_brands_tag_value_index";');
    this.addSql('alter table "query"."product_brands_tag" drop constraint "product_brands_tag_pkey";');
    this.addSql('alter table "query"."product_brands_tag" add constraint "product_brands_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_categories_properites_tag_value_index";');
    this.addSql('alter table "query"."product_categories_properites_tag" drop constraint "product_categories_properites_tag_pkey";');
    this.addSql('alter table "query"."product_categories_properites_tag" add constraint "product_categories_properites_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_categories_tag_value_index";');
    this.addSql('alter table "query"."product_categories_tag" drop constraint "product_categories_tag_pkey";');
    this.addSql('alter table "query"."product_categories_tag" add constraint "product_categories_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_checkers_tag_value_index";');
    this.addSql('alter table "query"."product_checkers_tag" drop constraint "product_checkers_tag_pkey";');
    this.addSql('alter table "query"."product_checkers_tag" add constraint "product_checkers_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_cities_tag_value_index";');
    this.addSql('alter table "query"."product_cities_tag" drop constraint "product_cities_tag_pkey";');
    this.addSql('alter table "query"."product_cities_tag" add constraint "product_cities_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_codes_tag_value_index";');
    this.addSql('alter table "query"."product_codes_tag" drop constraint "product_codes_tag_pkey";');
    this.addSql('alter table "query"."product_codes_tag" add constraint "product_codes_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_correctors_tag_value_index";');
    this.addSql('alter table "query"."product_correctors_tag" drop constraint "product_correctors_tag_pkey";');
    this.addSql('alter table "query"."product_correctors_tag" add constraint "product_correctors_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_countries_tag_value_index";');
    this.addSql('alter table "query"."product_countries_tag" drop constraint "product_countries_tag_pkey";');
    this.addSql('alter table "query"."product_countries_tag" add constraint "product_countries_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_data_quality_bugs_tag_value_index";');
    this.addSql('alter table "query"."product_data_quality_bugs_tag" drop constraint "product_data_quality_bugs_tag_pkey";');
    this.addSql('alter table "query"."product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_data_quality_errors_tag_value_index";');
    this.addSql('alter table "query"."product_data_quality_errors_tag" drop constraint "product_data_quality_errors_tag_pkey";');
    this.addSql('alter table "query"."product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_data_quality_tag_value_index";');
    this.addSql('alter table "query"."product_data_quality_tag" drop constraint "product_data_quality_tag_pkey";');
    this.addSql('alter table "query"."product_data_quality_tag" add constraint "product_data_quality_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_data_quality_warnings_tag_value_index";');
    this.addSql('alter table "query"."product_data_quality_warnings_tag" drop constraint "product_data_quality_warnings_tag_pkey";');
    this.addSql('alter table "query"."product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_data_sources_tag_value_index";');
    this.addSql('alter table "query"."product_data_sources_tag" drop constraint "product_data_sources_tag_pkey";');
    this.addSql('alter table "query"."product_data_sources_tag" add constraint "product_data_sources_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_debug_tag_value_index";');
    this.addSql('alter table "query"."product_debug_tag" drop constraint "product_debug_tag_pkey";');
    this.addSql('alter table "query"."product_debug_tag" add constraint "product_debug_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_ecoscore_tag_value_index";');
    this.addSql('alter table "query"."product_ecoscore_tag" drop constraint "product_ecoscore_tag_pkey";');
    this.addSql('alter table "query"."product_ecoscore_tag" add constraint "product_ecoscore_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_editors_tag_value_index";');
    this.addSql('alter table "query"."product_editors_tag" drop constraint "product_editors_tag_pkey";');
    this.addSql('alter table "query"."product_editors_tag" add constraint "product_editors_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_emb_codes_tag_value_index";');
    this.addSql('alter table "query"."product_emb_codes_tag" drop constraint "product_emb_codes_tag_pkey";');
    this.addSql('alter table "query"."product_emb_codes_tag" add constraint "product_emb_codes_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_entry_dates_tag_value_index";');
    this.addSql('alter table "query"."product_entry_dates_tag" drop constraint "product_entry_dates_tag_pkey";');
    this.addSql('alter table "query"."product_entry_dates_tag" add constraint "product_entry_dates_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_food_groups_tag_value_index";');
    this.addSql('alter table "query"."product_food_groups_tag" drop constraint "product_food_groups_tag_pkey";');
    this.addSql('alter table "query"."product_food_groups_tag" add constraint "product_food_groups_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_informers_tag_value_index";');
    this.addSql('alter table "query"."product_informers_tag" drop constraint "product_informers_tag_pkey";');
    this.addSql('alter table "query"."product_informers_tag" add constraint "product_informers_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_ingredients_analysis_tag_value_index";');
    this.addSql('alter table "query"."product_ingredients_analysis_tag" drop constraint "product_ingredients_analysis_tag_pkey";');
    this.addSql('alter table "query"."product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_ingredients_from_palm_oil_tag_value_index";');
    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" drop constraint "product_ingredients_from_palm_oil_tag_pkey";');
    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_ingredients_ntag_value_index";');
    this.addSql('alter table "query"."product_ingredients_ntag" drop constraint "product_ingredients_ntag_pkey";');
    this.addSql('alter table "query"."product_ingredients_ntag" add constraint "product_ingredients_ntag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_ingredients_original_tag_value_index";');
    this.addSql('alter table "query"."product_ingredients_original_tag" drop constraint "product_ingredients_original_tag_pkey";');
    this.addSql('alter table "query"."product_ingredients_original_tag" add constraint "product_ingredients_original_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_ingredients_tag_value_index";');
    this.addSql('alter table "query"."product_ingredients_tag" drop constraint "product_ingredients_tag_pkey";');
    this.addSql('alter table "query"."product_ingredients_tag" add constraint "product_ingredients_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_ingredients_that_may_be_from_palm_oil_tag_value_index";');
    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" drop constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey";');
    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_keywords_tag_value_index";');
    this.addSql('alter table "query"."product_keywords_tag" drop constraint "product_keywords_tag_pkey";');
    this.addSql('alter table "query"."product_keywords_tag" add constraint "product_keywords_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_labels_tag_value_index";');
    this.addSql('alter table "query"."product_labels_tag" drop constraint "product_labels_tag_pkey";');
    this.addSql('alter table "query"."product_labels_tag" add constraint "product_labels_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_languages_tag_value_index";');
    this.addSql('alter table "query"."product_languages_tag" drop constraint "product_languages_tag_pkey";');
    this.addSql('alter table "query"."product_languages_tag" add constraint "product_languages_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_last_check_dates_tag_value_index";');
    this.addSql('alter table "query"."product_last_check_dates_tag" drop constraint "product_last_check_dates_tag_pkey";');
    this.addSql('alter table "query"."product_last_check_dates_tag" add constraint "product_last_check_dates_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_last_edit_dates_tag_value_index";');
    this.addSql('alter table "query"."product_last_edit_dates_tag" drop constraint "product_last_edit_dates_tag_pkey";');
    this.addSql('alter table "query"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_latest_image_dates_tag_value_index";');
    this.addSql('alter table "query"."product_latest_image_dates_tag" drop constraint "product_latest_image_dates_tag_pkey";');
    this.addSql('alter table "query"."product_latest_image_dates_tag" add constraint "product_latest_image_dates_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_manufacturing_places_tag_value_index";');
    this.addSql('alter table "query"."product_manufacturing_places_tag" drop constraint "product_manufacturing_places_tag_pkey";');
    this.addSql('alter table "query"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_minerals_tag_value_index";');
    this.addSql('alter table "query"."product_minerals_tag" drop constraint "product_minerals_tag_pkey";');
    this.addSql('alter table "query"."product_minerals_tag" add constraint "product_minerals_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_misc_tag_value_index";');
    this.addSql('alter table "query"."product_misc_tag" drop constraint "product_misc_tag_pkey";');
    this.addSql('alter table "query"."product_misc_tag" add constraint "product_misc_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_nova_groups_tag_value_index";');
    this.addSql('alter table "query"."product_nova_groups_tag" drop constraint "product_nova_groups_tag_pkey";');
    this.addSql('alter table "query"."product_nova_groups_tag" add constraint "product_nova_groups_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_nucleotides_tag_value_index";');
    this.addSql('alter table "query"."product_nucleotides_tag" drop constraint "product_nucleotides_tag_pkey";');
    this.addSql('alter table "query"."product_nucleotides_tag" add constraint "product_nucleotides_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_nutrient_levels_tag_value_index";');
    this.addSql('alter table "query"."product_nutrient_levels_tag" drop constraint "product_nutrient_levels_tag_pkey";');
    this.addSql('alter table "query"."product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_nutriscore2021tag_value_index";');
    this.addSql('alter table "query"."product_nutriscore2021tag" drop constraint "product_nutriscore2021tag_pkey";');
    this.addSql('alter table "query"."product_nutriscore2021tag" add constraint "product_nutriscore2021tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_nutriscore2023tag_value_index";');
    this.addSql('alter table "query"."product_nutriscore2023tag" drop constraint "product_nutriscore2023tag_pkey";');
    this.addSql('alter table "query"."product_nutriscore2023tag" add constraint "product_nutriscore2023tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_nutriscore_tag_value_index";');
    this.addSql('alter table "query"."product_nutriscore_tag" drop constraint "product_nutriscore_tag_pkey";');
    this.addSql('alter table "query"."product_nutriscore_tag" add constraint "product_nutriscore_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_nutrition_grades_tag_value_index";');
    this.addSql('alter table "query"."product_nutrition_grades_tag" drop constraint "product_nutrition_grades_tag_pkey";');
    this.addSql('alter table "query"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_origins_tag_value_index";');
    this.addSql('alter table "query"."product_origins_tag" drop constraint "product_origins_tag_pkey";');
    this.addSql('alter table "query"."product_origins_tag" add constraint "product_origins_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_other_nutritional_substances_tag_value_index";');
    this.addSql('alter table "query"."product_other_nutritional_substances_tag" drop constraint "product_other_nutritional_substances_tag_pkey";');
    this.addSql('alter table "query"."product_other_nutritional_substances_tag" add constraint "product_other_nutritional_substances_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_packaging_materials_tag_value_index";');
    this.addSql('alter table "query"."product_packaging_materials_tag" drop constraint "product_packaging_materials_tag_pkey";');
    this.addSql('alter table "query"."product_packaging_materials_tag" add constraint "product_packaging_materials_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_packaging_recycling_tag_value_index";');
    this.addSql('alter table "query"."product_packaging_recycling_tag" drop constraint "product_packaging_recycling_tag_pkey";');
    this.addSql('alter table "query"."product_packaging_recycling_tag" add constraint "product_packaging_recycling_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_packaging_shapes_tag_value_index";');
    this.addSql('alter table "query"."product_packaging_shapes_tag" drop constraint "product_packaging_shapes_tag_pkey";');
    this.addSql('alter table "query"."product_packaging_shapes_tag" add constraint "product_packaging_shapes_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_packaging_tag_value_index";');
    this.addSql('alter table "query"."product_packaging_tag" drop constraint "product_packaging_tag_pkey";');
    this.addSql('alter table "query"."product_packaging_tag" add constraint "product_packaging_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_periods_after_opening_tag_value_index";');
    this.addSql('alter table "query"."product_periods_after_opening_tag" drop constraint "product_periods_after_opening_tag_pkey";');
    this.addSql('alter table "query"."product_periods_after_opening_tag" add constraint "product_periods_after_opening_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_photographers_tag_value_index";');
    this.addSql('alter table "query"."product_photographers_tag" drop constraint "product_photographers_tag_pkey";');
    this.addSql('alter table "query"."product_photographers_tag" add constraint "product_photographers_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_pnns_groups1tag_value_index";');
    this.addSql('alter table "query"."product_pnns_groups1tag" drop constraint "product_pnns_groups1tag_pkey";');
    this.addSql('alter table "query"."product_pnns_groups1tag" add constraint "product_pnns_groups1tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_pnns_groups2tag_value_index";');
    this.addSql('alter table "query"."product_pnns_groups2tag" drop constraint "product_pnns_groups2tag_pkey";');
    this.addSql('alter table "query"."product_pnns_groups2tag" add constraint "product_pnns_groups2tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_popularity_tag_value_index";');
    this.addSql('alter table "query"."product_popularity_tag" drop constraint "product_popularity_tag_pkey";');
    this.addSql('alter table "query"."product_popularity_tag" add constraint "product_popularity_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_purchase_places_tag_value_index";');
    this.addSql('alter table "query"."product_purchase_places_tag" drop constraint "product_purchase_places_tag_pkey";');
    this.addSql('alter table "query"."product_purchase_places_tag" add constraint "product_purchase_places_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_states_tag_value_index";');
    this.addSql('alter table "query"."product_states_tag" drop constraint "product_states_tag_pkey";');
    this.addSql('alter table "query"."product_states_tag" add constraint "product_states_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_stores_tag_value_index";');
    this.addSql('alter table "query"."product_stores_tag" drop constraint "product_stores_tag_pkey";');
    this.addSql('alter table "query"."product_stores_tag" add constraint "product_stores_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_teams_tag_value_index";');
    this.addSql('alter table "query"."product_teams_tag" drop constraint "product_teams_tag_pkey";');
    this.addSql('alter table "query"."product_teams_tag" add constraint "product_teams_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_traces_tag_value_index";');
    this.addSql('alter table "query"."product_traces_tag" drop constraint "product_traces_tag_pkey";');
    this.addSql('alter table "query"."product_traces_tag" add constraint "product_traces_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_unknown_nutrients_tag_value_index";');
    this.addSql('alter table "query"."product_unknown_nutrients_tag" drop constraint "product_unknown_nutrients_tag_pkey";');
    this.addSql('alter table "query"."product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_vitamins_tag_value_index";');
    this.addSql('alter table "query"."product_vitamins_tag" drop constraint "product_vitamins_tag_pkey";');
    this.addSql('alter table "query"."product_vitamins_tag" add constraint "product_vitamins_tag_pkey" primary key ("value", "product_id");');

    this.addSql('drop index "query"."product_weighers_tag_value_index";');
    this.addSql('alter table "query"."product_weighers_tag" drop constraint "product_weighers_tag_pkey";');
    this.addSql('alter table "query"."product_weighers_tag" add constraint "product_weighers_tag_pkey" primary key ("value", "product_id");');
  }

}
