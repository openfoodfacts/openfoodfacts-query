import { Migration } from '@mikro-orm/migrations';

export class Migration20250213104257 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."country" alter column "code" type text using ("code"::text);');
    this.addSql('alter table "query"."country" alter column "code" drop not null;');
    // Insert a few countries for tests. Rest will be inserted in main in addAllCountries
    this.addSql(`INSERT INTO country (code, tag) VALUES ('world','en:world'), ('fr','en:france'), ('uk','en:united-kingdom')`);
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."country" alter column "code" type text using ("code"::text);');
    this.addSql('alter table "query"."country" alter column "code" set not null;');
  }

}
