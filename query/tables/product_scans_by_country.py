from typing import Dict
from query.database import create_record
from query.models.scan import ScanCounts, ProductScans
from query.tables.product_country import fixup_product_countries_for_products


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
    """ This is only currently used in tests """
    scan = await create_record(
        connection,
        "product_scans_by_country",
        product_id=product["id"],
        country_id=country["id"],
        year=year,
        unique_scans=unique_scans,
    )
    await fixup_product_countries_for_products(connection, [product["id"]])
    return scan


async def create_scans(connection, scans: ProductScans):
    scans_by_country = []
    for code, years in scans.root.items():
        for year, scan_counts in years.root.items():
            for country, count in scan_counts.unique_scans_n_by_country.root.items():
                # TODO: Normalize code
                scans_by_country.append([code, str(year), country, str(count)])

    if scans_by_country:
        inserted = await connection.fetchmany("""insert into product_scans_by_country (product_id, year, country_id, unique_scans) 
            select product.id, source.year::int, country.id, source.scans::int 
            from (values ($1, $2, $3, $4)) as source (code, year, country, scans)
            join product on product.code = source.code
            join country on country.code = source.country
            on conflict (product_id, year, country_id) 
            do update set unique_scans = excluded.unique_scans
            returning product_id""", scans_by_country)

        ids_updated = list({ i['product_id'] for i in inserted })
        # TODO: remove country entries that are not referenced by a counties_tag

        await fixup_product_countries_for_products(connection, ids_updated)
