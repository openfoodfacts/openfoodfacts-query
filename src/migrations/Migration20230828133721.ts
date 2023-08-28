import { Migration } from '@mikro-orm/migrations';

export class Migration20230828133721 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product" drop column "ingredients_text";',
    );
    this.addSql(
      'alter table "query"."product" drop column "nutrition_as_sold_per";',
    );
    this.addSql(
      'alter table "query"."product" drop column "nutrition_prepared_per";',
    );
    this.addSql('alter table "query"."product" drop column "serving_size";');
    this.addSql(
      'alter table "query"."product" drop column "serving_quantity";',
    );
  }

  async down(): Promise<void> {
    this.addSql(
      'alter table "query"."product" add column "ingredients_text" text null default null, add column "nutrition_as_sold_per" text null default null, add column "nutrition_prepared_per" text null default null, add column "serving_size" text null default null, add column "serving_quantity" float8 null default null;',
    );
  }
}
