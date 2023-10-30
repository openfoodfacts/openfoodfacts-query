import { Migration } from '@mikro-orm/migrations';

export class Migration20231030101011 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."loaded_tag" ("id" text not null, constraint "loaded_tag_pkey" primary key ("id"));',
    );
  }

  async down(): Promise<void> {
    this.addSql('drop table if exists "query"."loaded_tag" cascade;');
  }
}
