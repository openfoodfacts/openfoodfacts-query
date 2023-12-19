import { Migration } from '@mikro-orm/migrations';

export class Migration20231218145009 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."settings" add column "last_message_id" text null;',
    );
  }

  async down(): Promise<void> {
    this.addSql(
      'alter table "query"."settings" drop column "last_message_id";',
    );
  }
}
