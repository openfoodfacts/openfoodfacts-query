import { Migration } from '@mikro-orm/migrations';

export class Migration20240712164659 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."product" alter column "last_modified" type timestamptz using ("last_modified"::timestamptz);');
    this.addSql('alter table "query"."product" alter column "last_updated" type timestamptz using ("last_updated"::timestamptz);');

    this.addSql('alter table "query"."settings" alter column "last_modified" type timestamptz using ("last_modified"::timestamptz);');
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product" alter column "last_modified" type timestamp using ("last_modified"::timestamp);');
    this.addSql('alter table "query"."product" alter column "last_updated" type timestamp using ("last_updated"::timestamp);');

    this.addSql('alter table "query"."settings" alter column "last_modified" type timestamp using ("last_modified"::timestamp);');
  }

}
