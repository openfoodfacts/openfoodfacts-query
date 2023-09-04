import { Migration } from '@mikro-orm/migrations';

export class Migration20230904100447 extends Migration {
  async up(): Promise<void> {
    this.addSql('create schema if not exists "query";');

    this.addSql(
      'create table "query"."product" ("id" uuid not null, "data" jsonb null, "name" text null, "code" text null, "last_modified" timestamp null, "creator" text null, "owners_tags" text null, "last_update_id" uuid null, "obsolete" boolean not null default false, constraint "product_pkey" primary key ("id"));',
    );
    this.addSql(
      'create index "product_code_index" on "query"."product" ("code");',
    );
    this.addSql(
      'create index "product_last_update_id_index" on "query"."product" ("last_update_id");',
    );

    this.addSql(
      'create table "query"."product_additives_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_additives_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_additives_tag_value_index" on "query"."product_additives_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_allergens_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_allergens_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_allergens_tag_value_index" on "query"."product_allergens_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_amino_acids_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_amino_acids_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_amino_acids_tag_value_index" on "query"."product_amino_acids_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_brands_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_brands_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_brands_tag_value_index" on "query"."product_brands_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_categories_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_categories_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_categories_tag_value_index" on "query"."product_categories_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_countries_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_countries_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_countries_tag_value_index" on "query"."product_countries_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_data_sources_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_sources_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_data_sources_tag_value_index" on "query"."product_data_sources_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_ecoscore_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ecoscore_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_ecoscore_tag_value_index" on "query"."product_ecoscore_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_emb_codes_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_emb_codes_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_emb_codes_tag_value_index" on "query"."product_emb_codes_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_entry_dates_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_entry_dates_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_entry_dates_tag_value_index" on "query"."product_entry_dates_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_ingredients_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_ingredients_tag_value_index" on "query"."product_ingredients_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_labels_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_labels_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_labels_tag_value_index" on "query"."product_labels_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_languages_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_languages_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_languages_tag_value_index" on "query"."product_languages_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_last_check_dates_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_last_check_dates_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_last_check_dates_tag_value_index" on "query"."product_last_check_dates_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_last_edit_dates_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_last_edit_dates_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_last_edit_dates_tag_value_index" on "query"."product_last_edit_dates_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_manufacturing_places_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_manufacturing_places_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_manufacturing_places_tag_value_index" on "query"."product_manufacturing_places_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_minerals_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_minerals_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_minerals_tag_value_index" on "query"."product_minerals_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_misc_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_misc_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_misc_tag_value_index" on "query"."product_misc_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_nova_groups_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nova_groups_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_nova_groups_tag_value_index" on "query"."product_nova_groups_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_nucleotides_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nucleotides_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_nucleotides_tag_value_index" on "query"."product_nucleotides_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_nutrition_grades_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_nutrition_grades_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_nutrition_grades_tag_value_index" on "query"."product_nutrition_grades_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_origins_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_origins_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_origins_tag_value_index" on "query"."product_origins_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_other_nutritional_substances_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_other_nutritional_substances_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_other_nutritional_substances_tag_value_index" on "query"."product_other_nutritional_substances_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_packaging_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_packaging_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_packaging_tag_value_index" on "query"."product_packaging_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_states_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_states_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_states_tag_value_index" on "query"."product_states_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_teams_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_teams_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_teams_tag_value_index" on "query"."product_teams_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_traces_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_traces_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_traces_tag_value_index" on "query"."product_traces_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_vitamins_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_vitamins_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_vitamins_tag_value_index" on "query"."product_vitamins_tag" ("value");',
    );

    this.addSql(
      'alter table "query"."product_additives_tag" add constraint "product_additives_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_allergens_tag" add constraint "product_allergens_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_amino_acids_tag" add constraint "product_amino_acids_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_brands_tag" add constraint "product_brands_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_categories_tag" add constraint "product_categories_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_countries_tag" add constraint "product_countries_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_data_sources_tag" add constraint "product_data_sources_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_ecoscore_tag" add constraint "product_ecoscore_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_emb_codes_tag" add constraint "product_emb_codes_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_entry_dates_tag" add constraint "product_entry_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_ingredients_tag" add constraint "product_ingredients_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_labels_tag" add constraint "product_labels_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_languages_tag" add constraint "product_languages_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_last_check_dates_tag" add constraint "product_last_check_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_minerals_tag" add constraint "product_minerals_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_misc_tag" add constraint "product_misc_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_nova_groups_tag" add constraint "product_nova_groups_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_nucleotides_tag" add constraint "product_nucleotides_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_origins_tag" add constraint "product_origins_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_other_nutritional_substances_tag" add constraint "product_other_nutritional_substances_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_packaging_tag" add constraint "product_packaging_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_states_tag" add constraint "product_states_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_teams_tag" add constraint "product_teams_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_traces_tag" add constraint "product_traces_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_vitamins_tag" add constraint "product_vitamins_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );
  }
}
