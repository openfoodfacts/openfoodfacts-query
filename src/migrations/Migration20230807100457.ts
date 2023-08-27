import { Migration } from '@mikro-orm/migrations';

export class Migration20230807100457 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product_additives_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_allergens_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_amino_acids_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_brands_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_categories_properties_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_categories_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_checkers_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_cities_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_codes_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_correctors_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_countries_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_creator_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_data_quality_bugs_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_data_quality_errors_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_data_quality_info_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_data_quality_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_data_quality_warnings_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_data_sources_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_ecoscore_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_editors_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_emb_codes_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_entry_dates_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_food_groups_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_informers_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_ingredients_analysis_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_ingredients_from_palm_oil_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_ingredients_ntag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_ingredients_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_labels_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_languages_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_last_edit_dates_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_last_image_dates_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_manufacturing_places_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_minerals_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_misc_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_nova_groups_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_nucleotides_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_nutrient_levels_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_nutrition_grades_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_origins_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_packaging_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_photographers_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_pnns_groups1tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_pnns_groups2tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_popularity_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_purchase_places_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_quality_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_states_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_stores_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_teams_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_traces_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_unknown_nutrients_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_vitamins_tag" add column "obsolete" boolean not null default false;',
    );

    this.addSql(
      'alter table "query"."product_weighers_tag" add column "obsolete" boolean not null default false;',
    );
  }

  async down(): Promise<void> {
    this.addSql(
      'alter table "query"."product_additives_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_allergens_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_amino_acids_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_brands_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_categories_properties_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_categories_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_checkers_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_cities_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_codes_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_correctors_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_countries_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_creator_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_data_quality_bugs_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_data_quality_errors_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_data_quality_info_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_data_quality_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_data_quality_warnings_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_data_sources_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_ecoscore_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_editors_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_emb_codes_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_entry_dates_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_food_groups_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_informers_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_ingredients_analysis_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_ingredients_from_palm_oil_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_ingredients_ntag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_ingredients_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_ingredients_that_may_be_from_palm_oil_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_labels_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_languages_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_last_edit_dates_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_last_image_dates_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_manufacturing_places_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_minerals_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_misc_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_nova_groups_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_nucleotides_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_nutrient_levels_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_nutrition_grades_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_origins_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_packaging_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_photographers_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_pnns_groups1tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_pnns_groups2tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_popularity_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_purchase_places_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_quality_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_states_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_stores_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_teams_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_traces_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_unknown_nutrients_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_vitamins_tag" drop column "obsolete";',
    );

    this.addSql(
      'alter table "query"."product_weighers_tag" drop column "obsolete";',
    );
  }
}
