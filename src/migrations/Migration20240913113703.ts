import { Migration } from '@mikro-orm/migrations';

export class Migration20240913113703 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."product" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_additives_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_additives_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_allergens_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_allergens_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_amino_acids_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_amino_acids_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_brands_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_brands_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_categories_properites_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_categories_properites_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_categories_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_categories_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_checkers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_checkers_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_cities_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_cities_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_codes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_codes_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_correctors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_correctors_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_countries_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_countries_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_data_quality_bugs_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_bugs_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_data_quality_errors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_errors_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_data_quality_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_data_quality_warnings_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_warnings_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_data_sources_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_sources_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_debug_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_debug_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ecoscore_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ecoscore_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_editors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_editors_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_emb_codes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_emb_codes_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_entry_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_entry_dates_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_food_groups_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_food_groups_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_informers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_informers_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ingredient" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredient" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ingredients_analysis_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_analysis_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ingredients_ntag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_ntag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ingredients_original_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_original_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ingredients_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_keywords_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_keywords_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_labels_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_labels_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_languages_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_languages_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_last_check_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_last_check_dates_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_last_edit_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_last_edit_dates_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_latest_image_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_latest_image_dates_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_manufacturing_places_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_manufacturing_places_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_minerals_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_minerals_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_misc_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_misc_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_nova_groups_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nova_groups_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_nucleotides_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nucleotides_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_nutrient_levels_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutrient_levels_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_nutriscore2021tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutriscore2021tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_nutriscore2023tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutriscore2023tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_nutriscore_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutriscore_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_nutrition_grades_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutrition_grades_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_origins_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_origins_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_other_nutritional_substances_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_other_nutritional_substances_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_packaging_materials_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_materials_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_packaging_recycling_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_recycling_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_packaging_shapes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_shapes_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_packaging_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_periods_after_opening_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_periods_after_opening_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_photographers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_photographers_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_pnns_groups1tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_pnns_groups1tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_pnns_groups2tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_pnns_groups2tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_popularity_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_popularity_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_purchase_places_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_purchase_places_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_states_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_states_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_stores_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_stores_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_teams_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_teams_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_traces_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_traces_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_unknown_nutrients_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_unknown_nutrients_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_vitamins_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_vitamins_tag" alter column "obsolete" drop not null;');

    this.addSql('alter table "query"."product_weighers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_weighers_tag" alter column "obsolete" drop not null;');
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_additives_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_additives_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_allergens_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_allergens_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_amino_acids_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_amino_acids_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_brands_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_brands_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_categories_properites_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_categories_properites_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_categories_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_categories_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_checkers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_checkers_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_cities_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_cities_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_codes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_codes_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_correctors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_correctors_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_countries_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_countries_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_data_quality_bugs_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_bugs_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_data_quality_errors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_errors_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_data_quality_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_data_quality_warnings_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_quality_warnings_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_data_sources_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_data_sources_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_debug_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_debug_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ecoscore_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ecoscore_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_editors_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_editors_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_emb_codes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_emb_codes_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_entry_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_entry_dates_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_food_groups_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_food_groups_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_informers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_informers_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ingredient" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredient" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ingredients_analysis_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_analysis_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_from_palm_oil_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ingredients_ntag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_ntag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ingredients_original_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_original_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ingredients_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_keywords_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_keywords_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_labels_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_labels_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_languages_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_languages_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_last_check_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_last_check_dates_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_last_edit_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_last_edit_dates_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_latest_image_dates_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_latest_image_dates_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_manufacturing_places_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_manufacturing_places_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_minerals_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_minerals_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_misc_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_misc_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_nova_groups_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nova_groups_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_nucleotides_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nucleotides_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_nutrient_levels_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutrient_levels_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_nutriscore2021tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutriscore2021tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_nutriscore2023tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutriscore2023tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_nutriscore_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutriscore_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_nutrition_grades_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_nutrition_grades_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_origins_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_origins_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_other_nutritional_substances_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_other_nutritional_substances_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_packaging_materials_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_materials_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_packaging_recycling_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_recycling_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_packaging_shapes_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_shapes_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_packaging_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_packaging_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_periods_after_opening_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_periods_after_opening_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_photographers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_photographers_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_pnns_groups1tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_pnns_groups1tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_pnns_groups2tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_pnns_groups2tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_popularity_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_popularity_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_purchase_places_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_purchase_places_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_states_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_states_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_stores_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_stores_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_teams_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_teams_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_traces_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_traces_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_unknown_nutrients_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_unknown_nutrients_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_vitamins_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_vitamins_tag" alter column "obsolete" set not null;');

    this.addSql('alter table "query"."product_weighers_tag" alter column "obsolete" type boolean using ("obsolete"::boolean);');
    this.addSql('alter table "query"."product_weighers_tag" alter column "obsolete" set not null;');
  }

}
