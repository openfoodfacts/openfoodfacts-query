import { Migration } from '@mikro-orm/migrations';

export class Migration20230814134214 extends Migration {

  async up(): Promise<void> {
    this.addSql('create table "off"."product_last_check_dates_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_last_check_dates_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_last_check_dates_tag_value_index" on "off"."product_last_check_dates_tag" ("value");');

    this.addSql('create table "off"."product_other_nutritional_substances_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_other_nutritional_substances_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_other_nutritional_substances_tag_value_index" on "off"."product_other_nutritional_substances_tag" ("value");');

    this.addSql('alter table "off"."product_last_check_dates_tag" add constraint "product_last_check_dates_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_other_nutritional_substances_tag" add constraint "product_other_nutritional_substances_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('drop table if exists "off"."product_categories_properties_tag" cascade;');

    this.addSql('drop table if exists "off"."product_checkers_tag" cascade;');

    this.addSql('drop table if exists "off"."product_cities_tag" cascade;');

    this.addSql('drop table if exists "off"."product_codes_tag" cascade;');

    this.addSql('drop table if exists "off"."product_correctors_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_bugs_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_errors_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_info_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_tag" cascade;');

    this.addSql('drop table if exists "off"."product_data_quality_warnings_tag" cascade;');

    this.addSql('drop table if exists "off"."product_editors_tag" cascade;');

    this.addSql('drop table if exists "off"."product_food_groups_tag" cascade;');

    this.addSql('drop table if exists "off"."product_informers_tag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_analysis_tag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_from_palm_oil_tag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_ntag" cascade;');

    this.addSql('drop table if exists "off"."product_ingredients_that_may_be_from_palm_oil_tag" cascade;');

    this.addSql('drop table if exists "off"."product_last_image_dates_tag" cascade;');

    this.addSql('drop table if exists "off"."product_nutrient_levels_tag" cascade;');

    this.addSql('drop table if exists "off"."product_photographers_tag" cascade;');

    this.addSql('drop table if exists "off"."product_pnns_groups1tag" cascade;');

    this.addSql('drop table if exists "off"."product_pnns_groups2tag" cascade;');

    this.addSql('drop table if exists "off"."product_popularity_tag" cascade;');

    this.addSql('drop table if exists "off"."product_purchase_places_tag" cascade;');

    this.addSql('drop table if exists "off"."product_quality_tag" cascade;');

    this.addSql('drop table if exists "off"."product_stores_tag" cascade;');

    this.addSql('drop table if exists "off"."product_unknown_nutrients_tag" cascade;');

    this.addSql('drop table if exists "off"."product_weighers_tag" cascade;');
  }

  async down(): Promise<void> {
    this.addSql('create table "off"."product_categories_properties_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_categories_properties_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_categories_properties_tag_value_index" on "off"."product_categories_properties_tag" ("value");');

    this.addSql('create table "off"."product_checkers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_checkers_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_checkers_tag_value_index" on "off"."product_checkers_tag" ("value");');

    this.addSql('create table "off"."product_cities_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_cities_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_cities_tag_value_index" on "off"."product_cities_tag" ("value");');

    this.addSql('create table "off"."product_codes_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_codes_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_codes_tag_value_index" on "off"."product_codes_tag" ("value");');

    this.addSql('create table "off"."product_correctors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_correctors_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_correctors_tag_value_index" on "off"."product_correctors_tag" ("value");');

    this.addSql('create table "off"."product_data_quality_bugs_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_bugs_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_data_quality_bugs_tag_value_index" on "off"."product_data_quality_bugs_tag" ("value");');

    this.addSql('create table "off"."product_data_quality_errors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_errors_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_data_quality_errors_tag_value_index" on "off"."product_data_quality_errors_tag" ("value");');

    this.addSql('create table "off"."product_data_quality_info_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_info_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_data_quality_info_tag_value_index" on "off"."product_data_quality_info_tag" ("value");');

    this.addSql('create table "off"."product_data_quality_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_data_quality_tag_value_index" on "off"."product_data_quality_tag" ("value");');

    this.addSql('create table "off"."product_data_quality_warnings_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_warnings_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_data_quality_warnings_tag_value_index" on "off"."product_data_quality_warnings_tag" ("value");');

    this.addSql('create table "off"."product_editors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_editors_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_editors_tag_value_index" on "off"."product_editors_tag" ("value");');

    this.addSql('create table "off"."product_food_groups_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_food_groups_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_food_groups_tag_value_index" on "off"."product_food_groups_tag" ("value");');

    this.addSql('create table "off"."product_informers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_informers_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_informers_tag_value_index" on "off"."product_informers_tag" ("value");');

    this.addSql('create table "off"."product_ingredients_analysis_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_analysis_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_ingredients_analysis_tag_value_index" on "off"."product_ingredients_analysis_tag" ("value");');

    this.addSql('create table "off"."product_ingredients_from_palm_oil_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_from_palm_oil_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_ingredients_from_palm_oil_tag_value_index" on "off"."product_ingredients_from_palm_oil_tag" ("value");');

    this.addSql('create table "off"."product_ingredients_ntag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_ntag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_ingredients_ntag_value_index" on "off"."product_ingredients_ntag" ("value");');

    this.addSql('create table "off"."product_ingredients_that_may_be_from_palm_oil_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_that_may_be_from_palm_oil_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_ingredients_that_may_be_from_palm_oil_tag_value_index" on "off"."product_ingredients_that_may_be_from_palm_oil_tag" ("value");');

    this.addSql('create table "off"."product_last_image_dates_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_last_image_dates_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_last_image_dates_tag_value_index" on "off"."product_last_image_dates_tag" ("value");');

    this.addSql('create table "off"."product_nutrient_levels_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nutrient_levels_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_nutrient_levels_tag_value_index" on "off"."product_nutrient_levels_tag" ("value");');

    this.addSql('create table "off"."product_photographers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_photographers_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_photographers_tag_value_index" on "off"."product_photographers_tag" ("value");');

    this.addSql('create table "off"."product_pnns_groups1tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_pnns_groups1tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_pnns_groups1tag_value_index" on "off"."product_pnns_groups1tag" ("value");');

    this.addSql('create table "off"."product_pnns_groups2tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_pnns_groups2tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_pnns_groups2tag_value_index" on "off"."product_pnns_groups2tag" ("value");');

    this.addSql('create table "off"."product_popularity_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_popularity_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_popularity_tag_value_index" on "off"."product_popularity_tag" ("value");');

    this.addSql('create table "off"."product_purchase_places_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_purchase_places_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_purchase_places_tag_value_index" on "off"."product_purchase_places_tag" ("value");');

    this.addSql('create table "off"."product_quality_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_quality_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_quality_tag_value_index" on "off"."product_quality_tag" ("value");');

    this.addSql('create table "off"."product_stores_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_stores_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_stores_tag_value_index" on "off"."product_stores_tag" ("value");');

    this.addSql('create table "off"."product_unknown_nutrients_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_unknown_nutrients_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_unknown_nutrients_tag_value_index" on "off"."product_unknown_nutrients_tag" ("value");');

    this.addSql('create table "off"."product_weighers_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_weighers_tag_pkey" primary key ("product_id", "value"));');
    this.addSql('create index "product_weighers_tag_value_index" on "off"."product_weighers_tag" ("value");');

    this.addSql('alter table "off"."product_categories_properties_tag" add constraint "product_categories_properties_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_checkers_tag" add constraint "product_checkers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_cities_tag" add constraint "product_cities_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_codes_tag" add constraint "product_codes_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_correctors_tag" add constraint "product_correctors_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_bugs_tag" add constraint "product_data_quality_bugs_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_info_tag" add constraint "product_data_quality_info_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_tag" add constraint "product_data_quality_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_data_quality_warnings_tag" add constraint "product_data_quality_warnings_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_editors_tag" add constraint "product_editors_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_food_groups_tag" add constraint "product_food_groups_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_informers_tag" add constraint "product_informers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_analysis_tag" add constraint "product_ingredients_analysis_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_from_palm_oil_tag" add constraint "product_ingredients_from_palm_oil_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_ntag" add constraint "product_ingredients_ntag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_ingredients_that_may_be_from_palm_oil_tag" add constraint "product_ingredients_that_may_be_from_palm_oil_tag_c5e4a_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_last_image_dates_tag" add constraint "product_last_image_dates_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_nutrient_levels_tag" add constraint "product_nutrient_levels_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_photographers_tag" add constraint "product_photographers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_pnns_groups1tag" add constraint "product_pnns_groups1tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_pnns_groups2tag" add constraint "product_pnns_groups2tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_popularity_tag" add constraint "product_popularity_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_purchase_places_tag" add constraint "product_purchase_places_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_quality_tag" add constraint "product_quality_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_stores_tag" add constraint "product_stores_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_unknown_nutrients_tag" add constraint "product_unknown_nutrients_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_weighers_tag" add constraint "product_weighers_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('drop table if exists "off"."product_last_check_dates_tag" cascade;');

    this.addSql('drop table if exists "off"."product_other_nutritional_substances_tag" cascade;');
  }

}
