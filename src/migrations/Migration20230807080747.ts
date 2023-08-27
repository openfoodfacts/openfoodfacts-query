import { Migration } from '@mikro-orm/migrations';

export class Migration20230807080747 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "obsolete" boolean not null default false;',
    );
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product" drop column "obsolete";');
  }
}
