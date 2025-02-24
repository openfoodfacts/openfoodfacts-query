import { Migration } from '@mikro-orm/migrations';

export class Migration20250224131357 extends Migration {
  async up(): Promise<void> {
    // Country table
    this.addSql(
      'create table "query"."country" ("id" serial primary key, "code" text null, "tag" text not null);',
    );
    this.addSql(
      'alter table "query"."country" add constraint "country_code_unique" unique ("code");',
    );
    this.addSql(
      'alter table "query"."country" add constraint "country_tag_unique" unique ("tag");',
    );
    // Insert world countries for tests.
    this.addSql(`INSERT INTO country (code, tag) VALUES ('world','en:world')`);
    // Create countries from existing data
    this.addSql(`INSERT INTO country (tag)
        SELECT DISTINCT pct.value
        FROM product_countries_tag pct
        WHERE NOT EXISTS (SELECT * FROM country WHERE tag = pct.value)
        ON CONFLICT (tag) DO NOTHING`);

    // Product scans by country
    this.addSql(
      'create table "query"."product_scans_by_country" ("product_id" int not null, "year" smallint not null, "country_id" int not null, "unique_scans" int not null, constraint "product_scans_by_country_pkey" primary key ("product_id", "year", "country_id"));',
    );
    this.addSql(
      'alter table "query"."product_scans_by_country" add constraint "product_scans_by_country_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );
    this.addSql(
      'alter table "query"."product_scans_by_country" add constraint "product_scans_by_country_country_id_foreign" foreign key ("country_id") references "query"."country" ("id") on update cascade on delete cascade;',
    );

    // Product country
    this.addSql(
      'create table "query"."product_country" ("product_id" int not null, "obsolete" boolean null, "country_id" int not null, "recent_scans" int not null, "total_scans" int not null, constraint "product_country_pkey" primary key ("product_id", "country_id"));',
    );
    this.addSql(
      'alter table "query"."product_country" add constraint "product_country_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;',
    );
    this.addSql(
      'alter table "query"."product_country" add constraint "product_country_country_id_foreign" foreign key ("country_id") references "query"."country" ("id") on update cascade on delete cascade;',
    );
    // Create product country entries for existing products
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
    this.addSql('drop table if exists "query"."product_country" cascade;');
    this.addSql(
      'drop table if exists "query"."product_scans_by_country" cascade;',
    );
    this.addSql('drop table if exists "query"."country" cascade;');
  }
}
