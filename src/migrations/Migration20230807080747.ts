import { Migration } from '@mikro-orm/migrations';

export class Migration20230807080747 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "off"."product" add column "obsolete" boolean not null default false;');
  }

  async down(): Promise<void> {
    this.addSql('alter table "off"."product" drop column "obsolete";');
  }

}
