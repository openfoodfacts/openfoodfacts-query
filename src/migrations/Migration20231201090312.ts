import { Migration } from '@mikro-orm/migrations';

export class Migration20231201090312 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."product_ingredient" alter column "percent" type text using ("percent"::text);');
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product_ingredient" alter column "percent" type double precision using ("percent"::double precision);');
  }

}
