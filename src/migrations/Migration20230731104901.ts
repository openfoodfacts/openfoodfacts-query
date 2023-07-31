import { Migration } from '@mikro-orm/migrations';

export class Migration20230731104901 extends Migration {

  async up(): Promise<void> {
    this.addSql('create table "off"."product_additives_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_additives_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_allergens_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_allergens_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_amino_acids_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_amino_acids_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_brands_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_brands_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_categories_properties_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_categories_properties_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_categories_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_categories_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_checkers_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_checkers_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_cities_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_cities_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_codes_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_codes_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_correctors_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_correctors_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_countries_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_countries_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_creator_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_creator_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_data_quality_bugs_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_data_quality_bugs_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_data_quality_errors_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_data_quality_errors_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_data_quality_info_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_data_quality_info_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_data_quality_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_data_quality_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_data_quality_warnings_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_data_quality_warnings_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_data_sources_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_data_sources_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_editors_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_editors_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_emb_codes_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_emb_codes_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_entry_dates_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_entry_dates_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_food_groups_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_food_groups_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_informers_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_informers_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_ingredients_analysis_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_ingredients_analysis_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_ingredients_from_palm_oil_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_ingredients_ntag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_ingredients_ntag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_ingredients_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_ingredients_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_ingredients_that_may_be_from_palm_oil_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_labels_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_labels_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_languages_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_languages_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_last_edit_dates_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_last_edit_dates_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_last_image_dates_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_last_image_dates_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_manufacturing_places_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_manufacturing_places_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_minerals_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_minerals_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_misc_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_misc_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_nova_groups_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_nova_groups_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_nucleotides_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_nucleotides_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_nutrient_levels_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_nutrient_levels_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_origins_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_origins_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_packaging_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_packaging_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_photographers_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_photographers_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_pnns_groups1tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_pnns_groups1tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_pnns_groups2tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_pnns_groups2tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_popularity_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_popularity_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_purchase_places_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_purchase_places_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_quality_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_quality_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_states_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_states_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_stores_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_stores_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_teams_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_teams_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_traces_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_traces_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_unknown_nutrients_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_unknown_nutrients_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_vitamins_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_vitamins_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_weighers_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_weighers_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('alter table "off"."product_additives_tag" add constraint "product_additives_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_allergens_tag" add constraint "product_allergens_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_amino_acids_tag" add constraint "product_amino_acids_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_brands_tag" add constraint "product_brands_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_categories_properties_tag" add constraint "product_categories_properties_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_categories_tag" add constraint "product_categories_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_checkers_tag" add constraint "product_checkers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_cities_tag" add constraint "product_cities_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_codes_tag" add constraint "product_codes_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_correctors_tag" add constraint "product_correctors_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_countries_tag" add constraint "product_countries_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_creator_tag" add constraint "product_creator_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_info_tag" add constraint "product_data_quality_info_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_tag" add constraint "product_data_quality_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_sources_tag" add constraint "product_data_sources_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_editors_tag" add constraint "product_editors_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_emb_codes_tag" add constraint "product_emb_codes_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_entry_dates_tag" add constraint "product_entry_dates_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_food_groups_tag" add constraint "product_food_groups_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_informers_tag" add constraint "product_informers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_ntag" add constraint "product_ingredients_ntag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_tag" add constraint "product_ingredients_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_c5e4a_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_labels_tag" add constraint "product_labels_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_languages_tag" add constraint "product_languages_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_last_image_dates_tag" add constraint "product_last_image_dates_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_minerals_tag" add constraint "product_minerals_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_misc_tag" add constraint "product_misc_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_nova_groups_tag" add constraint "product_nova_groups_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_nucleotides_tag" add constraint "product_nucleotides_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_origins_tag" add constraint "product_origins_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_packaging_tag" add constraint "product_packaging_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_photographers_tag" add constraint "product_photographers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_pnns_groups1tag" add constraint "product_pnns_groups1tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_pnns_groups2tag" add constraint "product_pnns_groups2tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_popularity_tag" add constraint "product_popularity_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_purchase_places_tag" add constraint "product_purchase_places_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_quality_tag" add constraint "product_quality_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_states_tag" add constraint "product_states_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_stores_tag" add constraint "product_stores_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_teams_tag" add constraint "product_teams_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_traces_tag" add constraint "product_traces_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_vitamins_tag" add constraint "product_vitamins_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_weighers_tag" add constraint "product_weighers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');
  }

  async down(): Promise<void> {
    this.addSql('drop table if exists "off"."product_additives_tag" cascade;');

    this.addSql('drop table if exists "off"."product_allergens_tag" cascade;');

    this.addSql('drop table if exists "off"."product_amino_acids_tag" cascade;');

    this.addSql('drop table if exists "off"."product_brands_tag" cascade;');

    this.addSql('drop table if exists "off"."product_categories_properties_tag" cascade;');

    this.addSql('drop table if exists "off"."product_categories_tag" cascade;');

    this.addSql('drop table if exists "off"."product_checkers_tag" cascade;');

    this.addSql('drop table if exists "off"."product_cities_tag" cascade;');

    this.addSql('drop table if exists "off"."product_codes_tag" cascade;');

    this.addSql('drop table if exists "off"."product_correctors_tag" cascade;');

    this.addSql('drop table if exists "off"."product_countries_tag" cascade;');

    this.addSql('drop table if exists "off"."product_creator_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_bugs_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_errors_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_info_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_warnings_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_sources_tag" cascade;');

    this.addSql('drop table if exists "off"."product_editors_tag" cascade;');

    this.addSql('drop table if exists "off"."product_emb_codes_tag" cascade;');

    this.addSql('drop table if exists "off"."product_entry_dates_tag" cascade;');

    this.addSql('drop table if exists "off"."product_food_groups_tag" cascade;');

    this.addSql('drop table if exists "off"."product_informers_tag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_analysis_tag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_from_palm_oil_tag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_ntag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_tag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_that_may_be_from_palm_oil_tag" cascade;');

    this.addSql('drop table if exists "off"."product_labels_tag" cascade;');

    this.addSql('drop table if exists "off"."product_languages_tag" cascade;');

    this.addSql('drop table if exists "off"."product_last_edit_dates_tag" cascade;');

    this.addSql('drop table if exists "off"."product_last_image_dates_tag" cascade;');

    this.addSql('drop table if exists "off"."product_manufacturing_places_tag" cascade;');

    this.addSql('drop table if exists "off"."product_minerals_tag" cascade;');

    this.addSql('drop table if exists "off"."product_misc_tag" cascade;');

    this.addSql('drop table if exists "off"."product_nova_groups_tag" cascade;');

    this.addSql('drop table if exists "off"."product_nucleotides_tag" cascade;');

    this.addSql('drop table if exists "off"."product_nutrient_levels_tag" cascade;');

    this.addSql('drop table if exists "off"."product_origins_tag" cascade;');

    this.addSql('drop table if exists "off"."product_packaging_tag" cascade;');

    this.addSql('drop table if exists "off"."product_photographers_tag" cascade;');

    this.addSql('drop table if exists "off"."product_pnns_groups1tag" cascade;');

    this.addSql('drop table if exists "off"."product_pnns_groups2tag" cascade;');

    this.addSql('drop table if exists "off"."product_popularity_tag" cascade;');

    this.addSql('drop table if exists "off"."product_purchase_places_tag" cascade;');

    this.addSql('drop table if exists "off"."product_quality_tag" cascade;');

    this.addSql('drop table if exists "off"."product_states_tag" cascade;');

    this.addSql('drop table if exists "off"."product_stores_tag" cascade;');

    this.addSql('drop table if exists "off"."product_teams_tag" cascade;');

    this.addSql('drop table if exists "off"."product_traces_tag" cascade;');

    this.addSql('drop table if exists "off"."product_unknown_nutrients_tag" cascade;');

    this.addSql('drop table if exists "off"."product_vitamins_tag" cascade;');

    this.addSql('drop table if exists "off"."product_weighers_tag" cascade;');
  }

}
