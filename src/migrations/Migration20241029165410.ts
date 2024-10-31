import { Migration } from '@mikro-orm/migrations';

export class Migration20241029165410 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."product" rename column "last_updated" to "last_processed";');
    this.addSql('alter table "query"."product" rename column "last_modified" to "last_updated";');
    this.addSql('alter table "query"."settings" rename column "last_modified" to "last_updated";');
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."settings" rename column "last_updated" to "last_modified";');
    this.addSql('alter table "query"."product" rename column "last_updated" to "last_modified";');
    this.addSql('alter table "query"."product" rename column "last_processed" to "last_updated";');
  }
}
