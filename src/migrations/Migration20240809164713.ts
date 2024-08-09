import { Migration } from '@mikro-orm/migrations';

export class Migration20240809164713 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "revision" int null;',
    );
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product" drop column "revision";');
  }
}
