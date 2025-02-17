import { Migration } from '@mikro-orm/migrations';

export class Migration20250213102704 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."country" add column "tag" text not null;');
    this.addSql('alter table "query"."country" add constraint "country_tag_unique" unique ("tag");');
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."country" drop constraint "country_tag_unique";');
    this.addSql('alter table "query"."country" drop column "tag";');
  }

}
