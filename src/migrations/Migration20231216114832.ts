import { Migration } from '@mikro-orm/migrations';

export class Migration20231216114832 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "last_updated" timestamp null, add column "source" varchar(255) null;',
    );
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product" drop column "last_updated";');
    this.addSql('alter table "query"."product" drop column "source";');
  }
}
