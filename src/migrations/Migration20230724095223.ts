import { Migration } from '@mikro-orm/migrations';

export class Migration20230724095223 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "off"."product" add column "last_modified" timestamp null;');
  }

  async down(): Promise<void> {
    this.addSql('alter table "off"."product" drop column "last_modified";');
  }

}
