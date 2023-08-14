import { Migration } from '@mikro-orm/migrations';

export class Migration20230814105020 extends Migration {

  async up(): Promise<void> {
    this.addSql('create index "product_additives_tag_value_index" on "off"."product_additives_tag" ("value");');

    this.addSql('create index "product_allergens_tag_value_index" on "off"."product_allergens_tag" ("value");');

    this.addSql('create index "product_amino_acids_tag_value_index" on "off"."product_amino_acids_tag" ("value");');

    this.addSql('create index "product_brands_tag_value_index" on "off"."product_brands_tag" ("value");');

    this.addSql('create index "product_categories_properties_tag_value_index" on "off"."product_categories_properties_tag" ("value");');

    this.addSql('create index "product_categories_tag_value_index" on "off"."product_categories_tag" ("value");');

    this.addSql('create index "product_checkers_tag_value_index" on "off"."product_checkers_tag" ("value");');

    this.addSql('create index "product_cities_tag_value_index" on "off"."product_cities_tag" ("value");');

    this.addSql('create index "product_codes_tag_value_index" on "off"."product_codes_tag" ("value");');

    this.addSql('create index "product_correctors_tag_value_index" on "off"."product_correctors_tag" ("value");');

    this.addSql('create index "product_countries_tag_value_index" on "off"."product_countries_tag" ("value");');

    this.addSql('create index "product_creator_tag_value_index" on "off"."product_creator_tag" ("value");');

    this.addSql('create index "product_data_quality_bugs_tag_value_index" on "off"."product_data_quality_bugs_tag" ("value");');

    this.addSql('create index "product_data_quality_errors_tag_value_index" on "off"."product_data_quality_errors_tag" ("value");');

    this.addSql('create index "product_data_quality_info_tag_value_index" on "off"."product_data_quality_info_tag" ("value");');

    this.addSql('create index "product_data_quality_tag_value_index" on "off"."product_data_quality_tag" ("value");');

    this.addSql('create index "product_data_quality_warnings_tag_value_index" on "off"."product_data_quality_warnings_tag" ("value");');

    this.addSql('create index "product_data_sources_tag_value_index" on "off"."product_data_sources_tag" ("value");');

    this.addSql('create index "product_ecoscore_tag_value_index" on "off"."product_ecoscore_tag" ("value");');

    this.addSql('create index "product_editors_tag_value_index" on "off"."product_editors_tag" ("value");');

    this.addSql('create index "product_emb_codes_tag_value_index" on "off"."product_emb_codes_tag" ("value");');

    this.addSql('create index "product_entry_dates_tag_value_index" on "off"."product_entry_dates_tag" ("value");');

    this.addSql('create index "product_food_groups_tag_value_index" on "off"."product_food_groups_tag" ("value");');

    this.addSql('create index "product_informers_tag_value_index" on "off"."product_informers_tag" ("value");');

    this.addSql('create index "product_ingredients_analysis_tag_value_index" on "off"."product_ingredients_analysis_tag" ("value");');

    this.addSql('create index "product_ingredients_from_palm_oil_tag_value_index" on "off"."product_ingredients_from_palm_oil_tag" ("value");');

    this.addSql('create index "product_ingredients_ntag_value_index" on "off"."product_ingredients_ntag" ("value");');

    this.addSql('create index "product_ingredients_tag_value_index" on "off"."product_ingredients_tag" ("value");');

    this.addSql('create index "product_ingredients_that_may_be_from_palm_oil_tag_value_index" on "off"."product_ingredients_that_may_be_from_palm_oil_tag" ("value");');

    this.addSql('create index "product_labels_tag_value_index" on "off"."product_labels_tag" ("value");');

    this.addSql('create index "product_languages_tag_value_index" on "off"."product_languages_tag" ("value");');

    this.addSql('create index "product_last_edit_dates_tag_value_index" on "off"."product_last_edit_dates_tag" ("value");');

    this.addSql('create index "product_last_image_dates_tag_value_index" on "off"."product_last_image_dates_tag" ("value");');

    this.addSql('create index "product_manufacturing_places_tag_value_index" on "off"."product_manufacturing_places_tag" ("value");');

    this.addSql('create index "product_minerals_tag_value_index" on "off"."product_minerals_tag" ("value");');

    this.addSql('create index "product_misc_tag_value_index" on "off"."product_misc_tag" ("value");');

    this.addSql('create index "product_nova_groups_tag_value_index" on "off"."product_nova_groups_tag" ("value");');

    this.addSql('create index "product_nucleotides_tag_value_index" on "off"."product_nucleotides_tag" ("value");');

    this.addSql('create index "product_nutrient_levels_tag_value_index" on "off"."product_nutrient_levels_tag" ("value");');

    this.addSql('create index "product_nutrition_grades_tag_value_index" on "off"."product_nutrition_grades_tag" ("value");');

    this.addSql('create index "product_origins_tag_value_index" on "off"."product_origins_tag" ("value");');

    this.addSql('create index "product_packaging_tag_value_index" on "off"."product_packaging_tag" ("value");');

    this.addSql('create index "product_photographers_tag_value_index" on "off"."product_photographers_tag" ("value");');

    this.addSql('create index "product_pnns_groups1tag_value_index" on "off"."product_pnns_groups1tag" ("value");');

    this.addSql('create index "product_pnns_groups2tag_value_index" on "off"."product_pnns_groups2tag" ("value");');

    this.addSql('create index "product_popularity_tag_value_index" on "off"."product_popularity_tag" ("value");');

    this.addSql('create index "product_purchase_places_tag_value_index" on "off"."product_purchase_places_tag" ("value");');

    this.addSql('create index "product_quality_tag_value_index" on "off"."product_quality_tag" ("value");');

    this.addSql('create index "product_states_tag_value_index" on "off"."product_states_tag" ("value");');

    this.addSql('create index "product_stores_tag_value_index" on "off"."product_stores_tag" ("value");');

    this.addSql('create index "product_teams_tag_value_index" on "off"."product_teams_tag" ("value");');

    this.addSql('create index "product_traces_tag_value_index" on "off"."product_traces_tag" ("value");');

    this.addSql('create index "product_unknown_nutrients_tag_value_index" on "off"."product_unknown_nutrients_tag" ("value");');

    this.addSql('create index "product_vitamins_tag_value_index" on "off"."product_vitamins_tag" ("value");');

    this.addSql('create index "product_weighers_tag_value_index" on "off"."product_weighers_tag" ("value");');
  }

  async down(): Promise<void> {
    this.addSql('drop index "off"."product_additives_tag_value_index";');

    this.addSql('drop index "off"."product_allergens_tag_value_index";');

    this.addSql('drop index "off"."product_amino_acids_tag_value_index";');

    this.addSql('drop index "off"."product_brands_tag_value_index";');

    this.addSql('drop index "off"."product_categories_properties_tag_value_index";');

    this.addSql('drop index "off"."product_categories_tag_value_index";');

    this.addSql('drop index "off"."product_checkers_tag_value_index";');

    this.addSql('drop index "off"."product_cities_tag_value_index";');

    this.addSql('drop index "off"."product_codes_tag_value_index";');

    this.addSql('drop index "off"."product_correctors_tag_value_index";');

    this.addSql('drop index "off"."product_countries_tag_value_index";');

    this.addSql('drop index "off"."product_creator_tag_value_index";');

    this.addSql('drop index "off"."product_data_quality_bugs_tag_value_index";');

    this.addSql('drop index "off"."product_data_quality_errors_tag_value_index";');

    this.addSql('drop index "off"."product_data_quality_info_tag_value_index";');

    this.addSql('drop index "off"."product_data_quality_tag_value_index";');

    this.addSql('drop index "off"."product_data_quality_warnings_tag_value_index";');

    this.addSql('drop index "off"."product_data_sources_tag_value_index";');

    this.addSql('drop index "off"."product_ecoscore_tag_value_index";');

    this.addSql('drop index "off"."product_editors_tag_value_index";');

    this.addSql('drop index "off"."product_emb_codes_tag_value_index";');

    this.addSql('drop index "off"."product_entry_dates_tag_value_index";');

    this.addSql('drop index "off"."product_food_groups_tag_value_index";');

    this.addSql('drop index "off"."product_informers_tag_value_index";');

    this.addSql('drop index "off"."product_ingredients_analysis_tag_value_index";');

    this.addSql('drop index "off"."product_ingredients_from_palm_oil_tag_value_index";');

    this.addSql('drop index "off"."product_ingredients_ntag_value_index";');

    this.addSql('drop index "off"."product_ingredients_tag_value_index";');

    this.addSql('drop index "off"."product_ingredients_that_may_be_from_palm_oil_tag_value_index";');

    this.addSql('drop index "off"."product_labels_tag_value_index";');

    this.addSql('drop index "off"."product_languages_tag_value_index";');

    this.addSql('drop index "off"."product_last_edit_dates_tag_value_index";');

    this.addSql('drop index "off"."product_last_image_dates_tag_value_index";');

    this.addSql('drop index "off"."product_manufacturing_places_tag_value_index";');

    this.addSql('drop index "off"."product_minerals_tag_value_index";');

    this.addSql('drop index "off"."product_misc_tag_value_index";');

    this.addSql('drop index "off"."product_nova_groups_tag_value_index";');

    this.addSql('drop index "off"."product_nucleotides_tag_value_index";');

    this.addSql('drop index "off"."product_nutrient_levels_tag_value_index";');

    this.addSql('drop index "off"."product_nutrition_grades_tag_value_index";');

    this.addSql('drop index "off"."product_origins_tag_value_index";');

    this.addSql('drop index "off"."product_packaging_tag_value_index";');

    this.addSql('drop index "off"."product_photographers_tag_value_index";');

    this.addSql('drop index "off"."product_pnns_groups1tag_value_index";');

    this.addSql('drop index "off"."product_pnns_groups2tag_value_index";');

    this.addSql('drop index "off"."product_popularity_tag_value_index";');

    this.addSql('drop index "off"."product_purchase_places_tag_value_index";');

    this.addSql('drop index "off"."product_quality_tag_value_index";');

    this.addSql('drop index "off"."product_states_tag_value_index";');

    this.addSql('drop index "off"."product_stores_tag_value_index";');

    this.addSql('drop index "off"."product_teams_tag_value_index";');

    this.addSql('drop index "off"."product_traces_tag_value_index";');

    this.addSql('drop index "off"."product_unknown_nutrients_tag_value_index";');

    this.addSql('drop index "off"."product_vitamins_tag_value_index";');

    this.addSql('drop index "off"."product_weighers_tag_value_index";');
  }

}
