import { Migration } from '@mikro-orm/migrations';

export class Migration20230814105020 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create index "product_additives_tag_value_index" on "query"."product_additives_tag" ("value");',
    );

    this.addSql(
      'create index "product_allergens_tag_value_index" on "query"."product_allergens_tag" ("value");',
    );

    this.addSql(
      'create index "product_amino_acids_tag_value_index" on "query"."product_amino_acids_tag" ("value");',
    );

    this.addSql(
      'create index "product_brands_tag_value_index" on "query"."product_brands_tag" ("value");',
    );

    this.addSql(
      'create index "product_categories_properties_tag_value_index" on "query"."product_categories_properties_tag" ("value");',
    );

    this.addSql(
      'create index "product_categories_tag_value_index" on "query"."product_categories_tag" ("value");',
    );

    this.addSql(
      'create index "product_checkers_tag_value_index" on "query"."product_checkers_tag" ("value");',
    );

    this.addSql(
      'create index "product_cities_tag_value_index" on "query"."product_cities_tag" ("value");',
    );

    this.addSql(
      'create index "product_codes_tag_value_index" on "query"."product_codes_tag" ("value");',
    );

    this.addSql(
      'create index "product_correctors_tag_value_index" on "query"."product_correctors_tag" ("value");',
    );

    this.addSql(
      'create index "product_countries_tag_value_index" on "query"."product_countries_tag" ("value");',
    );

    this.addSql(
      'create index "product_creator_tag_value_index" on "query"."product_creator_tag" ("value");',
    );

    this.addSql(
      'create index "product_data_quality_bugs_tag_value_index" on "query"."product_data_quality_bugs_tag" ("value");',
    );

    this.addSql(
      'create index "product_data_quality_errors_tag_value_index" on "query"."product_data_quality_errors_tag" ("value");',
    );

    this.addSql(
      'create index "product_data_quality_info_tag_value_index" on "query"."product_data_quality_info_tag" ("value");',
    );

    this.addSql(
      'create index "product_data_quality_tag_value_index" on "query"."product_data_quality_tag" ("value");',
    );

    this.addSql(
      'create index "product_data_quality_warnings_tag_value_index" on "query"."product_data_quality_warnings_tag" ("value");',
    );

    this.addSql(
      'create index "product_data_sources_tag_value_index" on "query"."product_data_sources_tag" ("value");',
    );

    this.addSql(
      'create index "product_ecoscore_tag_value_index" on "query"."product_ecoscore_tag" ("value");',
    );

    this.addSql(
      'create index "product_editors_tag_value_index" on "query"."product_editors_tag" ("value");',
    );

    this.addSql(
      'create index "product_emb_codes_tag_value_index" on "query"."product_emb_codes_tag" ("value");',
    );

    this.addSql(
      'create index "product_entry_dates_tag_value_index" on "query"."product_entry_dates_tag" ("value");',
    );

    this.addSql(
      'create index "product_food_groups_tag_value_index" on "query"."product_food_groups_tag" ("value");',
    );

    this.addSql(
      'create index "product_informers_tag_value_index" on "query"."product_informers_tag" ("value");',
    );

    this.addSql(
      'create index "product_ingredients_analysis_tag_value_index" on "query"."product_ingredients_analysis_tag" ("value");',
    );

    this.addSql(
      'create index "product_ingredients_from_palm_oil_tag_value_index" on "query"."product_ingredients_from_palm_oil_tag" ("value");',
    );

    this.addSql(
      'create index "product_ingredients_ntag_value_index" on "query"."product_ingredients_ntag" ("value");',
    );

    this.addSql(
      'create index "product_ingredients_tag_value_index" on "query"."product_ingredients_tag" ("value");',
    );

    this.addSql(
      'create index "product_ingredients_that_may_be_from_palm_oil_tag_value_index" on "query"."product_ingredients_that_may_be_from_palm_oil_tag" ("value");',
    );

    this.addSql(
      'create index "product_labels_tag_value_index" on "query"."product_labels_tag" ("value");',
    );

    this.addSql(
      'create index "product_languages_tag_value_index" on "query"."product_languages_tag" ("value");',
    );

    this.addSql(
      'create index "product_last_edit_dates_tag_value_index" on "query"."product_last_edit_dates_tag" ("value");',
    );

    this.addSql(
      'create index "product_last_image_dates_tag_value_index" on "query"."product_last_image_dates_tag" ("value");',
    );

    this.addSql(
      'create index "product_manufacturing_places_tag_value_index" on "query"."product_manufacturing_places_tag" ("value");',
    );

    this.addSql(
      'create index "product_minerals_tag_value_index" on "query"."product_minerals_tag" ("value");',
    );

    this.addSql(
      'create index "product_misc_tag_value_index" on "query"."product_misc_tag" ("value");',
    );

    this.addSql(
      'create index "product_nova_groups_tag_value_index" on "query"."product_nova_groups_tag" ("value");',
    );

    this.addSql(
      'create index "product_nucleotides_tag_value_index" on "query"."product_nucleotides_tag" ("value");',
    );

    this.addSql(
      'create index "product_nutrient_levels_tag_value_index" on "query"."product_nutrient_levels_tag" ("value");',
    );

    this.addSql(
      'create index "product_nutrition_grades_tag_value_index" on "query"."product_nutrition_grades_tag" ("value");',
    );

    this.addSql(
      'create index "product_origins_tag_value_index" on "query"."product_origins_tag" ("value");',
    );

    this.addSql(
      'create index "product_packaging_tag_value_index" on "query"."product_packaging_tag" ("value");',
    );

    this.addSql(
      'create index "product_photographers_tag_value_index" on "query"."product_photographers_tag" ("value");',
    );

    this.addSql(
      'create index "product_pnns_groups1tag_value_index" on "query"."product_pnns_groups1tag" ("value");',
    );

    this.addSql(
      'create index "product_pnns_groups2tag_value_index" on "query"."product_pnns_groups2tag" ("value");',
    );

    this.addSql(
      'create index "product_popularity_tag_value_index" on "query"."product_popularity_tag" ("value");',
    );

    this.addSql(
      'create index "product_purchase_places_tag_value_index" on "query"."product_purchase_places_tag" ("value");',
    );

    this.addSql(
      'create index "product_quality_tag_value_index" on "query"."product_quality_tag" ("value");',
    );

    this.addSql(
      'create index "product_states_tag_value_index" on "query"."product_states_tag" ("value");',
    );

    this.addSql(
      'create index "product_stores_tag_value_index" on "query"."product_stores_tag" ("value");',
    );

    this.addSql(
      'create index "product_teams_tag_value_index" on "query"."product_teams_tag" ("value");',
    );

    this.addSql(
      'create index "product_traces_tag_value_index" on "query"."product_traces_tag" ("value");',
    );

    this.addSql(
      'create index "product_unknown_nutrients_tag_value_index" on "query"."product_unknown_nutrients_tag" ("value");',
    );

    this.addSql(
      'create index "product_vitamins_tag_value_index" on "query"."product_vitamins_tag" ("value");',
    );

    this.addSql(
      'create index "product_weighers_tag_value_index" on "query"."product_weighers_tag" ("value");',
    );
  }

  async down(): Promise<void> {
    this.addSql('drop index "query"."product_additives_tag_value_index";');

    this.addSql('drop index "query"."product_allergens_tag_value_index";');

    this.addSql('drop index "query"."product_amino_acids_tag_value_index";');

    this.addSql('drop index "query"."product_brands_tag_value_index";');

    this.addSql(
      'drop index "query"."product_categories_properties_tag_value_index";',
    );

    this.addSql('drop index "query"."product_categories_tag_value_index";');

    this.addSql('drop index "query"."product_checkers_tag_value_index";');

    this.addSql('drop index "query"."product_cities_tag_value_index";');

    this.addSql('drop index "query"."product_codes_tag_value_index";');

    this.addSql('drop index "query"."product_correctors_tag_value_index";');

    this.addSql('drop index "query"."product_countries_tag_value_index";');

    this.addSql('drop index "query"."product_creator_tag_value_index";');

    this.addSql(
      'drop index "query"."product_data_quality_bugs_tag_value_index";',
    );

    this.addSql(
      'drop index "query"."product_data_quality_errors_tag_value_index";',
    );

    this.addSql(
      'drop index "query"."product_data_quality_info_tag_value_index";',
    );

    this.addSql('drop index "query"."product_data_quality_tag_value_index";');

    this.addSql(
      'drop index "query"."product_data_quality_warnings_tag_value_index";',
    );

    this.addSql('drop index "query"."product_data_sources_tag_value_index";');

    this.addSql('drop index "query"."product_ecoscore_tag_value_index";');

    this.addSql('drop index "query"."product_editors_tag_value_index";');

    this.addSql('drop index "query"."product_emb_codes_tag_value_index";');

    this.addSql('drop index "query"."product_entry_dates_tag_value_index";');

    this.addSql('drop index "query"."product_food_groups_tag_value_index";');

    this.addSql('drop index "query"."product_informers_tag_value_index";');

    this.addSql(
      'drop index "query"."product_ingredients_analysis_tag_value_index";',
    );

    this.addSql(
      'drop index "query"."product_ingredients_from_palm_oil_tag_value_index";',
    );

    this.addSql('drop index "query"."product_ingredients_ntag_value_index";');

    this.addSql('drop index "query"."product_ingredients_tag_value_index";');

    this.addSql(
      'drop index "query"."product_ingredients_that_may_be_from_palm_oil_tag_value_index";',
    );

    this.addSql('drop index "query"."product_labels_tag_value_index";');

    this.addSql('drop index "query"."product_languages_tag_value_index";');

    this.addSql(
      'drop index "query"."product_last_edit_dates_tag_value_index";',
    );

    this.addSql(
      'drop index "query"."product_last_image_dates_tag_value_index";',
    );

    this.addSql(
      'drop index "query"."product_manufacturing_places_tag_value_index";',
    );

    this.addSql('drop index "query"."product_minerals_tag_value_index";');

    this.addSql('drop index "query"."product_misc_tag_value_index";');

    this.addSql('drop index "query"."product_nova_groups_tag_value_index";');

    this.addSql('drop index "query"."product_nucleotides_tag_value_index";');

    this.addSql(
      'drop index "query"."product_nutrient_levels_tag_value_index";',
    );

    this.addSql(
      'drop index "query"."product_nutrition_grades_tag_value_index";',
    );

    this.addSql('drop index "query"."product_origins_tag_value_index";');

    this.addSql('drop index "query"."product_packaging_tag_value_index";');

    this.addSql('drop index "query"."product_photographers_tag_value_index";');

    this.addSql('drop index "query"."product_pnns_groups1tag_value_index";');

    this.addSql('drop index "query"."product_pnns_groups2tag_value_index";');

    this.addSql('drop index "query"."product_popularity_tag_value_index";');

    this.addSql(
      'drop index "query"."product_purchase_places_tag_value_index";',
    );

    this.addSql('drop index "query"."product_quality_tag_value_index";');

    this.addSql('drop index "query"."product_states_tag_value_index";');

    this.addSql('drop index "query"."product_stores_tag_value_index";');

    this.addSql('drop index "query"."product_teams_tag_value_index";');

    this.addSql('drop index "query"."product_traces_tag_value_index";');

    this.addSql(
      'drop index "query"."product_unknown_nutrients_tag_value_index";',
    );

    this.addSql('drop index "query"."product_vitamins_tag_value_index";');

    this.addSql('drop index "query"."product_weighers_tag_value_index";');
  }
}
