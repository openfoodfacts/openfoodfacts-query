import { Migration } from '@mikro-orm/migrations';

export class Migration20230828144607 extends Migration {
  async up(): Promise<void> {
    this.addSql('drop table if exists "query"."product_creator_tag" cascade;');
  }

  async down(): Promise<void> {
    this.addSql(
      'create table "query"."product_creator_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_creator_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_creator_tag_value_index" on "query"."product_creator_tag" ("value");',
    );

    this.addSql(
      'alter table "query"."product_creator_tag" add constraint "product_creator_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;',
    );
  }
}
