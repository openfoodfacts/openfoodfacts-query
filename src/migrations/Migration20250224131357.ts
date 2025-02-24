import { Migration } from '@mikro-orm/migrations';

export class Migration20250224131357 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'alter table "query"."product_country" add column "obsolete" boolean null;',
    );

    // Create country entries for existing products
    this
      .addSql(`INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT pct.product_id, pct.obsolete, c.id, 0, 0
        FROM product_countries_tag pct
        JOIN country c ON c.tag = pct.value
        ON CONFLICT (product_id, country_id) DO NOTHING`);

    // Create world entries for existing products
    this
      .addSql(`INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT p.id, p.obsolete, c.id, 0, 0
        FROM product p, country c
        WHERE c.tag = 'en:world'
        ON CONFLICT (product_id, country_id) DO NOTHING`);

    this.addSql(
      'create index product_country_ix1 on product_country (obsolete, country_id, recent_scans DESC, total_scans DESC, product_id);',
    );
  }

  async down(): Promise<void> {
    this.addSql(
      'alter table "query"."product_country" drop column "obsolete";',
    );
  }
}
