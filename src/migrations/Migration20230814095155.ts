import { Migration } from '@mikro-orm/migrations';

export class Migration20230814095155 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "off"."product_additives_tag" drop constraint "product_additives_tag_pkey";');
    this.addSql('alter table "off"."product_additives_tag" add constraint "product_additives_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_allergens_tag" drop constraint "product_allergens_tag_pkey";');
    this.addSql('alter table "off"."product_allergens_tag" add constraint "product_allergens_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_amino_acids_tag" drop constraint "product_amino_acids_tag_pkey";');
    this.addSql('alter table "off"."product_amino_acids_tag" add constraint "product_amino_acids_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_brands_tag" drop constraint "product_brands_tag_pkey";');
    this.addSql('alter table "off"."product_brands_tag" add constraint "product_brands_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_categories_properties_tag" drop constraint "product_categories_properties_tag_pkey";');
    this.addSql('alter table "off"."product_categories_properties_tag" add constraint "product_categories_properties_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_categories_tag" drop constraint "product_categories_tag_pkey";');
    this.addSql('alter table "off"."product_categories_tag" add constraint "product_categories_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_checkers_tag" drop constraint "product_checkers_tag_pkey";');
    this.addSql('alter table "off"."product_checkers_tag" add constraint "product_checkers_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_cities_tag" drop constraint "product_cities_tag_pkey";');
    this.addSql('alter table "off"."product_cities_tag" add constraint "product_cities_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_codes_tag" drop constraint "product_codes_tag_pkey";');
    this.addSql('alter table "off"."product_codes_tag" add constraint "product_codes_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_correctors_tag" drop constraint "product_correctors_tag_pkey";');
    this.addSql('alter table "off"."product_correctors_tag" add constraint "product_correctors_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_countries_tag" drop constraint "product_countries_tag_pkey";');
    this.addSql('alter table "off"."product_countries_tag" add constraint "product_countries_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_creator_tag" drop constraint "product_creator_tag_pkey";');
    this.addSql('alter table "off"."product_creator_tag" add constraint "product_creator_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_data_quality_bugs_tag" drop constraint "product_data_quality_bugs_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_data_quality_errors_tag" drop constraint "product_data_quality_errors_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_data_quality_info_tag" drop constraint "product_data_quality_info_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_info_tag" add constraint "product_data_quality_info_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_data_quality_tag" drop constraint "product_data_quality_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_tag" add constraint "product_data_quality_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_data_quality_warnings_tag" drop constraint "product_data_quality_warnings_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_data_sources_tag" drop constraint "product_data_sources_tag_pkey";');
    this.addSql('alter table "off"."product_data_sources_tag" add constraint "product_data_sources_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_ecoscore_tag" drop constraint "product_ecoscore_tag_pkey";');
    this.addSql('alter table "off"."product_ecoscore_tag" add constraint "product_ecoscore_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_editors_tag" drop constraint "product_editors_tag_pkey";');
    this.addSql('alter table "off"."product_editors_tag" add constraint "product_editors_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_emb_codes_tag" drop constraint "product_emb_codes_tag_pkey";');
    this.addSql('alter table "off"."product_emb_codes_tag" add constraint "product_emb_codes_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_entry_dates_tag" drop constraint "product_entry_dates_tag_pkey";');
    this.addSql('alter table "off"."product_entry_dates_tag" add constraint "product_entry_dates_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_food_groups_tag" drop constraint "product_food_groups_tag_pkey";');
    this.addSql('alter table "off"."product_food_groups_tag" add constraint "product_food_groups_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_informers_tag" drop constraint "product_informers_tag_pkey";');
    this.addSql('alter table "off"."product_informers_tag" add constraint "product_informers_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_ingredients_analysis_tag" drop constraint "product_ingredients_analysis_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_ingredients_from_palm_oil_tag" drop constraint "product_ingredients_from_palm_oil_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_ingredients_ntag" drop constraint "product_ingredients_ntag_pkey";');
    this.addSql('alter table "off"."product_ingredients_ntag" add constraint "product_ingredients_ntag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_ingredients_tag" drop constraint "product_ingredients_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_tag" add constraint "product_ingredients_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_ingredients_that_may_be_from_palm_oil_tag" drop constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_labels_tag" drop constraint "product_labels_tag_pkey";');
    this.addSql('alter table "off"."product_labels_tag" add constraint "product_labels_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_languages_tag" drop constraint "product_languages_tag_pkey";');
    this.addSql('alter table "off"."product_languages_tag" add constraint "product_languages_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_last_edit_dates_tag" drop constraint "product_last_edit_dates_tag_pkey";');
    this.addSql('alter table "off"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_last_image_dates_tag" drop constraint "product_last_image_dates_tag_pkey";');
    this.addSql('alter table "off"."product_last_image_dates_tag" add constraint "product_last_image_dates_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_manufacturing_places_tag" drop constraint "product_manufacturing_places_tag_pkey";');
    this.addSql('alter table "off"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_minerals_tag" drop constraint "product_minerals_tag_pkey";');
    this.addSql('alter table "off"."product_minerals_tag" add constraint "product_minerals_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_misc_tag" drop constraint "product_misc_tag_pkey";');
    this.addSql('alter table "off"."product_misc_tag" add constraint "product_misc_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_nova_groups_tag" drop constraint "product_nova_groups_tag_pkey";');
    this.addSql('alter table "off"."product_nova_groups_tag" add constraint "product_nova_groups_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_nucleotides_tag" drop constraint "product_nucleotides_tag_pkey";');
    this.addSql('alter table "off"."product_nucleotides_tag" add constraint "product_nucleotides_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_nutrient_levels_tag" drop constraint "product_nutrient_levels_tag_pkey";');
    this.addSql('alter table "off"."product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_nutrition_grades_tag" drop constraint "product_nutrition_grades_tag_pkey";');
    this.addSql('alter table "off"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_origins_tag" drop constraint "product_origins_tag_pkey";');
    this.addSql('alter table "off"."product_origins_tag" add constraint "product_origins_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_packaging_tag" drop constraint "product_packaging_tag_pkey";');
    this.addSql('alter table "off"."product_packaging_tag" add constraint "product_packaging_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_photographers_tag" drop constraint "product_photographers_tag_pkey";');
    this.addSql('alter table "off"."product_photographers_tag" add constraint "product_photographers_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_pnns_groups1tag" drop constraint "product_pnns_groups1tag_pkey";');
    this.addSql('alter table "off"."product_pnns_groups1tag" add constraint "product_pnns_groups1tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_pnns_groups2tag" drop constraint "product_pnns_groups2tag_pkey";');
    this.addSql('alter table "off"."product_pnns_groups2tag" add constraint "product_pnns_groups2tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_popularity_tag" drop constraint "product_popularity_tag_pkey";');
    this.addSql('alter table "off"."product_popularity_tag" add constraint "product_popularity_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_purchase_places_tag" drop constraint "product_purchase_places_tag_pkey";');
    this.addSql('alter table "off"."product_purchase_places_tag" add constraint "product_purchase_places_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_quality_tag" drop constraint "product_quality_tag_pkey";');
    this.addSql('alter table "off"."product_quality_tag" add constraint "product_quality_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_states_tag" drop constraint "product_states_tag_pkey";');
    this.addSql('alter table "off"."product_states_tag" add constraint "product_states_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_stores_tag" drop constraint "product_stores_tag_pkey";');
    this.addSql('alter table "off"."product_stores_tag" add constraint "product_stores_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_teams_tag" drop constraint "product_teams_tag_pkey";');
    this.addSql('alter table "off"."product_teams_tag" add constraint "product_teams_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_traces_tag" drop constraint "product_traces_tag_pkey";');
    this.addSql('alter table "off"."product_traces_tag" add constraint "product_traces_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_unknown_nutrients_tag" drop constraint "product_unknown_nutrients_tag_pkey";');
    this.addSql('alter table "off"."product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_vitamins_tag" drop constraint "product_vitamins_tag_pkey";');
    this.addSql('alter table "off"."product_vitamins_tag" add constraint "product_vitamins_tag_pkey" primary key ("product_id", "value");');

    this.addSql('alter table "off"."product_weighers_tag" drop constraint "product_weighers_tag_pkey";');
    this.addSql('alter table "off"."product_weighers_tag" add constraint "product_weighers_tag_pkey" primary key ("product_id", "value");');
  }

  async down(): Promise<void> {
    this.addSql('alter table "off"."product_additives_tag" drop constraint "product_additives_tag_pkey";');
    this.addSql('alter table "off"."product_additives_tag" add constraint "product_additives_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_allergens_tag" drop constraint "product_allergens_tag_pkey";');
    this.addSql('alter table "off"."product_allergens_tag" add constraint "product_allergens_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_amino_acids_tag" drop constraint "product_amino_acids_tag_pkey";');
    this.addSql('alter table "off"."product_amino_acids_tag" add constraint "product_amino_acids_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_brands_tag" drop constraint "product_brands_tag_pkey";');
    this.addSql('alter table "off"."product_brands_tag" add constraint "product_brands_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_categories_properties_tag" drop constraint "product_categories_properties_tag_pkey";');
    this.addSql('alter table "off"."product_categories_properties_tag" add constraint "product_categories_properties_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_categories_tag" drop constraint "product_categories_tag_pkey";');
    this.addSql('alter table "off"."product_categories_tag" add constraint "product_categories_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_checkers_tag" drop constraint "product_checkers_tag_pkey";');
    this.addSql('alter table "off"."product_checkers_tag" add constraint "product_checkers_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_cities_tag" drop constraint "product_cities_tag_pkey";');
    this.addSql('alter table "off"."product_cities_tag" add constraint "product_cities_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_codes_tag" drop constraint "product_codes_tag_pkey";');
    this.addSql('alter table "off"."product_codes_tag" add constraint "product_codes_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_correctors_tag" drop constraint "product_correctors_tag_pkey";');
    this.addSql('alter table "off"."product_correctors_tag" add constraint "product_correctors_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_countries_tag" drop constraint "product_countries_tag_pkey";');
    this.addSql('alter table "off"."product_countries_tag" add constraint "product_countries_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_creator_tag" drop constraint "product_creator_tag_pkey";');
    this.addSql('alter table "off"."product_creator_tag" add constraint "product_creator_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_data_quality_bugs_tag" drop constraint "product_data_quality_bugs_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_data_quality_errors_tag" drop constraint "product_data_quality_errors_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_data_quality_info_tag" drop constraint "product_data_quality_info_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_info_tag" add constraint "product_data_quality_info_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_data_quality_tag" drop constraint "product_data_quality_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_tag" add constraint "product_data_quality_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_data_quality_warnings_tag" drop constraint "product_data_quality_warnings_tag_pkey";');
    this.addSql('alter table "off"."product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_data_sources_tag" drop constraint "product_data_sources_tag_pkey";');
    this.addSql('alter table "off"."product_data_sources_tag" add constraint "product_data_sources_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_ecoscore_tag" drop constraint "product_ecoscore_tag_pkey";');
    this.addSql('alter table "off"."product_ecoscore_tag" add constraint "product_ecoscore_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_editors_tag" drop constraint "product_editors_tag_pkey";');
    this.addSql('alter table "off"."product_editors_tag" add constraint "product_editors_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_emb_codes_tag" drop constraint "product_emb_codes_tag_pkey";');
    this.addSql('alter table "off"."product_emb_codes_tag" add constraint "product_emb_codes_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_entry_dates_tag" drop constraint "product_entry_dates_tag_pkey";');
    this.addSql('alter table "off"."product_entry_dates_tag" add constraint "product_entry_dates_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_food_groups_tag" drop constraint "product_food_groups_tag_pkey";');
    this.addSql('alter table "off"."product_food_groups_tag" add constraint "product_food_groups_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_informers_tag" drop constraint "product_informers_tag_pkey";');
    this.addSql('alter table "off"."product_informers_tag" add constraint "product_informers_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_ingredients_analysis_tag" drop constraint "product_ingredients_analysis_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_ingredients_from_palm_oil_tag" drop constraint "product_ingredients_from_palm_oil_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_ingredients_ntag" drop constraint "product_ingredients_ntag_pkey";');
    this.addSql('alter table "off"."product_ingredients_ntag" add constraint "product_ingredients_ntag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_ingredients_tag" drop constraint "product_ingredients_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_tag" add constraint "product_ingredients_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_ingredients_that_may_be_from_palm_oil_tag" drop constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey";');
    this.addSql('alter table "off"."product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_labels_tag" drop constraint "product_labels_tag_pkey";');
    this.addSql('alter table "off"."product_labels_tag" add constraint "product_labels_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_languages_tag" drop constraint "product_languages_tag_pkey";');
    this.addSql('alter table "off"."product_languages_tag" add constraint "product_languages_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_last_edit_dates_tag" drop constraint "product_last_edit_dates_tag_pkey";');
    this.addSql('alter table "off"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_last_image_dates_tag" drop constraint "product_last_image_dates_tag_pkey";');
    this.addSql('alter table "off"."product_last_image_dates_tag" add constraint "product_last_image_dates_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_manufacturing_places_tag" drop constraint "product_manufacturing_places_tag_pkey";');
    this.addSql('alter table "off"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_minerals_tag" drop constraint "product_minerals_tag_pkey";');
    this.addSql('alter table "off"."product_minerals_tag" add constraint "product_minerals_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_misc_tag" drop constraint "product_misc_tag_pkey";');
    this.addSql('alter table "off"."product_misc_tag" add constraint "product_misc_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_nova_groups_tag" drop constraint "product_nova_groups_tag_pkey";');
    this.addSql('alter table "off"."product_nova_groups_tag" add constraint "product_nova_groups_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_nucleotides_tag" drop constraint "product_nucleotides_tag_pkey";');
    this.addSql('alter table "off"."product_nucleotides_tag" add constraint "product_nucleotides_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_nutrient_levels_tag" drop constraint "product_nutrient_levels_tag_pkey";');
    this.addSql('alter table "off"."product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_nutrition_grades_tag" drop constraint "product_nutrition_grades_tag_pkey";');
    this.addSql('alter table "off"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_origins_tag" drop constraint "product_origins_tag_pkey";');
    this.addSql('alter table "off"."product_origins_tag" add constraint "product_origins_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_packaging_tag" drop constraint "product_packaging_tag_pkey";');
    this.addSql('alter table "off"."product_packaging_tag" add constraint "product_packaging_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_photographers_tag" drop constraint "product_photographers_tag_pkey";');
    this.addSql('alter table "off"."product_photographers_tag" add constraint "product_photographers_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_pnns_groups1tag" drop constraint "product_pnns_groups1tag_pkey";');
    this.addSql('alter table "off"."product_pnns_groups1tag" add constraint "product_pnns_groups1tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_pnns_groups2tag" drop constraint "product_pnns_groups2tag_pkey";');
    this.addSql('alter table "off"."product_pnns_groups2tag" add constraint "product_pnns_groups2tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_popularity_tag" drop constraint "product_popularity_tag_pkey";');
    this.addSql('alter table "off"."product_popularity_tag" add constraint "product_popularity_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_purchase_places_tag" drop constraint "product_purchase_places_tag_pkey";');
    this.addSql('alter table "off"."product_purchase_places_tag" add constraint "product_purchase_places_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_quality_tag" drop constraint "product_quality_tag_pkey";');
    this.addSql('alter table "off"."product_quality_tag" add constraint "product_quality_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_states_tag" drop constraint "product_states_tag_pkey";');
    this.addSql('alter table "off"."product_states_tag" add constraint "product_states_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_stores_tag" drop constraint "product_stores_tag_pkey";');
    this.addSql('alter table "off"."product_stores_tag" add constraint "product_stores_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_teams_tag" drop constraint "product_teams_tag_pkey";');
    this.addSql('alter table "off"."product_teams_tag" add constraint "product_teams_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_traces_tag" drop constraint "product_traces_tag_pkey";');
    this.addSql('alter table "off"."product_traces_tag" add constraint "product_traces_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_unknown_nutrients_tag" drop constraint "product_unknown_nutrients_tag_pkey";');
    this.addSql('alter table "off"."product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_vitamins_tag" drop constraint "product_vitamins_tag_pkey";');
    this.addSql('alter table "off"."product_vitamins_tag" add constraint "product_vitamins_tag_pkey" primary key ("value", "product_id");');

    this.addSql('alter table "off"."product_weighers_tag" drop constraint "product_weighers_tag_pkey";');
    this.addSql('alter table "off"."product_weighers_tag" add constraint "product_weighers_tag_pkey" primary key ("value", "product_id");');
  }

}
