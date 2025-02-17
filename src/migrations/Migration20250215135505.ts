import { Migration } from '@mikro-orm/migrations';

export class Migration20250215135505 extends Migration {

  async up(): Promise<void> {
    this.addSql('drop table if exists "query"."product_scans" cascade;');
  }

  async down(): Promise<void> {
    this.addSql('create table "query"."product_scans" ("product_id" int not null, "year" smallint not null, "scans" int not null, "unique_scans" int not null, constraint "product_scans_pkey" primary key ("product_id", "year"));');

    this.addSql('alter table "query"."product_scans" add constraint "product_scans_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');
  }

}
