import { Migration } from '@mikro-orm/migrations';

export class Migration20230717172017 extends Migration {
  async up(): Promise<void> {
    this.addSql('create schema if not exists "off";');

    this.addSql(
      'create table "off"."product" ("id" uuid not null, "data" jsonb null, "name" text null, "search" tsvector null, "code" text null, "ingredients_text" text null, "nutrition_as_sold_per" text null, "nutrition_prepared_per" text null, "serving_size" text null, "serving_quantity" double precision null, constraint "product_pkey" primary key ("id"));',
    );
    this.addSql(
      'create index "product_code_index" on "off"."product" ("code");',
    );
    this.addSql(
      'create index "product_search_index" on "off"."product" using gin("search");',
    );

    this.addSql(
      'create table "off"."product_tag" ("product_id" uuid not null, "tag_type" text not null, "sequence" int not null, "value" text not null, constraint "product_tag_pkey" primary key ("product_id", "tag_type", "sequence"));',
    );
    this.addSql(
      'create index "product_tag_tag_type_value_product_id_index" on "off"."product_tag" ("tag_type", "value", "product_id");',
    );

    this.addSql(
      'alter table "off"."product_tag" add constraint "product_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;',
    );
  }
}
