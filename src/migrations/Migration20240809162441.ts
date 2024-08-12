import { Migration } from '@mikro-orm/migrations';

export class Migration20240809162441 extends Migration {

  async up(): Promise<void> {
    this.addSql('create index "product_creator_index" on "query"."product" ("creator");');
    this.addSql('create index "product_owners_tags_index" on "query"."product" ("owners_tags");');
  }

  async down(): Promise<void> {
    this.addSql('drop index "query"."product_creator_index";');
    this.addSql('drop index "query"."product_owners_tags_index";');
  }

}
