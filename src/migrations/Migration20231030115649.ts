import { Migration } from '@mikro-orm/migrations';

export class Migration20231030115649 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."product_codes_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_codes_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_codes_tag_value_index" on "query"."product_codes_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_data_quality_errors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_errors_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_data_quality_errors_tag_value_index" on "query"."product_data_quality_errors_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_data_quality_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_data_quality_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_data_quality_tag_value_index" on "query"."product_data_quality_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_editors_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_editors_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_editors_tag_value_index" on "query"."product_editors_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_ingredients_original_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_original_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_ingredients_original_tag_value_index" on "query"."product_ingredients_original_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_keywords_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_keywords_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_keywords_tag_value_index" on "query"."product_keywords_tag" ("value");',
    );

    this.addSql(
      'create table "query"."product_stores_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_stores_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_stores_tag_value_index" on "query"."product_stores_tag" ("value");',
    );

    this.addSql(
      'alter table "query"."product_codes_tag" add constraint "product_codes_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_data_quality_errors_tag" add constraint "product_data_quality_errors_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_data_quality_tag" add constraint "product_data_quality_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_editors_tag" add constraint "product_editors_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_ingredients_original_tag" add constraint "product_ingredients_original_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_keywords_tag" add constraint "product_keywords_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'alter table "query"."product_stores_tag" add constraint "product_stores_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );
  }

  async down(): Promise<void> {
    this.addSql('drop table if exists "query"."product_codes_tag" cascade;');

    this.addSql(
      'drop table if exists "query"."product_data_quality_errors_tag" cascade;',
    );

    this.addSql(
      'drop table if exists "query"."product_data_quality_tag" cascade;',
    );

    this.addSql('drop table if exists "query"."product_editors_tag" cascade;');

    this.addSql(
      'drop table if exists "query"."product_ingredients_original_tag" cascade;',
    );

    this.addSql('drop table if exists "query"."product_keywords_tag" cascade;');

    this.addSql('drop table if exists "query"."product_stores_tag" cascade;');
  }
}
