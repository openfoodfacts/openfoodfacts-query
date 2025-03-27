import { Migration } from '@mikro-orm/migrations';

export class Migration20241029165410 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product" rename column "last_updated" to "last_processed";',
    );
    this.addSql(
      'alter table "query"."product" rename column "last_modified" to "last_updated";',
    );
    this.addSql(
      'alter table "query"."settings" rename column "last_modified" to "last_updated";',
    );
    this.addSql(
      'alter table "query"."product" add column "process_id" bigint null;',
    );
    this.addSql(
      'create index "product_process_id_index" on "query"."product" ("process_id");',
    );
    this.addSql('drop index "query"."product_last_update_id_index";');
    this.addSql('alter table "query"."product" drop column "last_update_id";');
  }

  async down(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "last_update_id" uuid null;',
    );
    this.addSql(
      'create index "product_last_update_id_index" on "query"."product" ("last_update_id");',
    );
    this.addSql('drop index "query"."product_process_id_index";');
    this.addSql('alter table "query"."product" drop column "process_id";');
    this.addSql(
      'alter table "query"."settings" rename column "last_updated" to "last_modified";',
    );
    this.addSql(
      'alter table "query"."product" rename column "last_updated" to "last_modified";',
    );
    this.addSql(
      'alter table "query"."product" rename column "last_processed" to "last_updated";',
    );
  }
}
