import { Migration } from '@mikro-orm/migrations';

export class Migration20230724114052 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "creator" text null, add column "owners_tags" text null;',
    );
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product" drop column "creator";');
    this.addSql('alter table "query"."product" drop column "owners_tags";');
  }
}
