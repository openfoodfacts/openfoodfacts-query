import { Migration } from '@mikro-orm/migrations';

export class Migration20250220093406 extends Migration {

  async up(): Promise<void> {
    this.addSql('drop index "query"."product_scans_by_country_ix1";');
  }

  async down(): Promise<void> {
    this.addSql('create index product_scans_by_country_ix1 on product_scans_by_country (year, country_id, unique_scans DESC, product_id);');
  }

}
