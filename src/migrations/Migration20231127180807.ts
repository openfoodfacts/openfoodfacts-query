import { Migration } from '@mikro-orm/migrations';

export class Migration20231127180807 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."product_ingredient" ("product_id" uuid not null, "sequence" text not null, "parent_product_id" uuid null, "parent_sequence" text null, "ingredient_text" text null, "id" text null, "ciqual_food_code" text null, "percent_min" double precision null, "percent" double precision null, "percent_max" double precision null, "percent_estimate" double precision null, "data" json null, "obsolete" boolean not null default false, constraint "product_ingredient_pkey" primary key ("product_id", "sequence"));',
    );
    this.addSql(
      'create index "product_ingredient_parent_product_id_parent_sequence_index" on "query"."product_ingredient" ("parent_product_id", "parent_sequence");',
    );

    this.addSql(
      'alter table "query"."product_ingredient" add constraint "product_ingredient_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );
    this.addSql(
      'alter table "query"."product_ingredient" add constraint "product_ingredient_parent_product_id_parent_sequence_foreign" foreign key ("parent_product_id", "parent_sequence") references "query"."product_ingredient" ("product_id", "sequence") on update cascade on delete set null;',
    );

    this.addSql(
      'ALTER TABLE query.product ALTER COLUMN "data" TYPE json USING "data"::text::json;',
    );

    this.addSql(
      'alter table "query"."product" add column "ingredients_without_ciqual_codes_count" int null, add column "ingredients_count" int null;',
    );
  }

  async down(): Promise<void> {
    this.addSql(
      'alter table "query"."product_ingredient" drop constraint "product_ingredient_parent_product_id_parent_sequence_foreign";',
    );

    this.addSql('drop table if exists "query"."product_ingredient" cascade;');

    this.addSql(
      'ALTER TABLE query.product ALTER COLUMN "data" TYPE jsonb USING "data"::text::jsonb;',
    );

    this.addSql(
      'alter table "query"."product" drop column "ingredients_without_ciqual_codes_count";',
    );
    this.addSql(
      'alter table "query"."product" drop column "ingredients_count";',
    );
  }
}
