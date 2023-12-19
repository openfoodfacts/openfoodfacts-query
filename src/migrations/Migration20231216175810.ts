import { Migration } from '@mikro-orm/migrations';

export class Migration20231216175810 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."product_periods_after_opening_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_periods_after_opening_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_periods_after_opening_tag_value_index" on "query"."product_periods_after_opening_tag" ("value");',
    );

    this.addSql(
      'alter table "query"."product_periods_after_opening_tag" add constraint "product_periods_after_opening_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql('drop table if exists "query"."product_owners_tag" cascade;');
  }

  async down(): Promise<void> {
    this.addSql(
      'create table "query"."product_owners_tag" ("product_id" uuid not null, "value" text not null, "obsolete" boolean not null default false, constraint "product_owners_tag_pkey" primary key ("product_id", "value"));',
    );
    this.addSql(
      'create index "product_owners_tag_value_index" on "query"."product_owners_tag" ("value");',
    );

    this.addSql(
      'alter table "query"."product_owners_tag" add constraint "product_owners_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );

    this.addSql(
      'drop table if exists "query"."product_periods_after_opening_tag" cascade;',
    );
  }
}
