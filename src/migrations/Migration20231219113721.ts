import { Migration } from '@mikro-orm/migrations';

export class Migration20231219113721 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."product_ingredients_ntag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_ingredients_ntag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_ingredients_ntag_value_index" on "query"."product_ingredients_ntag" ("value");',
    );

    this.addSql(
      'alter table "query"."product_ingredients_ntag" add constraint "product_ingredients_ntag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );
  }

  async down(): Promise<void> {
    this.addSql(
      'drop table if exists "query"."product_ingredients_ntag" cascade;',
    );
  }
}
