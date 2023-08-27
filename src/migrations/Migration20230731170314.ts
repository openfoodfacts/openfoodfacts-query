import { Migration } from '@mikro-orm/migrations';

export class Migration20230731170314 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create index "product_last_update_id_index" on "query"."product" ("last_update_id");',
    );
  }

  async down(): Promise<void> {
    this.addSql('drop index "query"."product_last_update_id_index";');
  }
}
