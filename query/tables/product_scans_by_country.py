from query.database import create_record
from query.tables.product_country import fixup_product_countries_for_product


async def create_table(connection):
    await connection.execute(
        'create table "product_scans_by_country" ("product_id" int not null, "year" smallint not null, "country_id" int not null, "unique_scans" int not null, constraint "product_scans_by_country_pkey" primary key ("product_id", "year", "country_id"));',
    )
    await connection.execute(
        'alter table "product_scans_by_country" add constraint "product_scans_by_country_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
    await connection.execute(
        'alter table "product_scans_by_country" add constraint "product_scans_by_country_country_id_foreign" foreign key ("country_id") references "country" ("id") on update cascade on delete cascade;',
    )


async def create_scan(connection, product, country, year, unique_scans):
    scan = await create_record(connection, "product_scans_by_country", product_id=product['id'], country_id=country['id'], year=year, unique_scans=unique_scans)
    await fixup_product_countries_for_product(connection, product['id'])
    return scan
