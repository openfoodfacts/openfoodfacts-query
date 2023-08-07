import { Migration } from '@mikro-orm/migrations';

export class Migration20230731164608 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "off"."product" add column "last_update_id" uuid null;');
  }

  async down(): Promise<void> {
    this.addSql('alter table "off"."product" drop column "last_update_id";');
  }

}
