import { Migration } from '@mikro-orm/migrations';

export class Migration20230724095223 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "last_modified" timestamp null;',
    );
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product" drop column "last_modified";');
  }
}
