import { Migration } from '@mikro-orm/migrations';

export class Migration20250215141851 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."product_country" ("product_id" int not null, "country_id" int not null, "recent_scans" int not null, "total_scans" int not null, constraint "product_country_pkey" primary key ("product_id", "country_id"));',
    );

    // Create countries from existing data
    this.addSql(`INSERT INTO country (tag)
        SELECT DISTINCT pct.value
        FROM product_countries_tag pct
        WHERE NOT EXISTS (SELECT * FROM country WHERE tag = pct.value)
        ON CONFLICT (tag) DO NOTHING`);

    // Create country entries for existing products
    this
      .addSql(`INSERT INTO product_country (product_id, country_id, recent_scans, total_scans)
        SELECT pct.product_id, c.id, 0, 0
        FROM product_countries_tag pct
        JOIN country c ON c.tag = pct.value
        ON CONFLICT (product_id, country_id) DO NOTHING`);

    // Create world entries for existing products
    this
      .addSql(`INSERT INTO product_country (product_id, country_id, recent_scans, total_scans)
        SELECT p.id, c.id, 0, 0
        FROM product p, country c
        WHERE c.tag = 'en:world'
        ON CONFLICT (product_id, country_id) DO NOTHING`);

    this.addSql(
      'create index product_country_ix1 on product_country (country_id, recent_scans DESC, total_scans DESC, product_id);',
    );

    this.addSql(
      'alter table "query"."product_country" add constraint "product_country_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );
    this.addSql(
      'alter table "query"."product_country" add constraint "product_country_country_id_foreign" foreign key ("country_id") references "query"."country" ("id") on update cascade on delete cascade;',
    );
  }

  async down(): Promise<void> {
    this.addSql('drop table if exists "query"."product_country" cascade;');
  }
}
