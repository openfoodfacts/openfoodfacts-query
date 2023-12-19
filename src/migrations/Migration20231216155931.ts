import { Migration } from '@mikro-orm/migrations';

export class Migration20231216155931 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."settings" ("id" serial primary key, "last_modified" timestamp null);',
    );
  }

  async down(): Promise<void> {
    this.addSql('drop table if exists "query"."settings" cascade;');
  }
}
