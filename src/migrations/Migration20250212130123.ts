import { Migration } from '@mikro-orm/migrations';

export class Migration20250212130123 extends Migration {

  async up(): Promise<void> {
    this.addSql('create table "query"."country" ("id" serial primary key, "code" text not null);');
    this.addSql('alter table "query"."country" add constraint "country_code_unique" unique ("code");');

    this.addSql('create table "query"."product_scans" ("product_id" int not null, "year" smallint not null, "scans" int not null, "unique_scans" int not null, constraint "product_scans_pkey" primary key ("product_id", "year"));');

    this.addSql('create table "query"."product_scans_by_country" ("product_id" int not null, "year" smallint not null, "country_id" int not null, "unique_scans" int not null, constraint "product_scans_by_country_pkey" primary key ("product_id", "year", "country_id"));');
    this.addSql('create index product_scans_by_country_ix1 on product_scans_by_country (year, country_id, unique_scans DESC, product_id);');

    this.addSql('alter table "query"."product_scans" add constraint "product_scans_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_scans_by_country" add constraint "product_scans_by_country_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');
    this.addSql('alter table "query"."product_scans_by_country" add constraint "product_scans_by_country_country_id_foreign" foreign key ("country_id") references "query"."country" ("id") on update cascade on delete cascade;');
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product_scans_by_country" drop constraint "product_scans_by_country_country_id_foreign";');

    this.addSql('drop table if exists "query"."country" cascade;');

    this.addSql('drop table if exists "query"."product_scans" cascade;');

    this.addSql('drop table if exists "query"."product_scans_by_country" cascade;');
  }

}
