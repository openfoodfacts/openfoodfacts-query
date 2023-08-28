import { Migration } from '@mikro-orm/migrations';

export class Migration20230828134202 extends Migration {
  async up(): Promise<void> {
    this.addSql('drop index "query"."product_search_index";');
    this.addSql('alter table "query"."product" drop column "search";');
  }

  async down(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "search" tsvector null;',
    );
    this.addSql(
      'create index "product_search_index" on "query"."product" using gin("search");',
    );
  }
}
