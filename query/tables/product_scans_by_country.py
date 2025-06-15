"""The Number of scans for each product by country and year"""

from ..database import create_record
from ..models.scan import ProductScans
from ..tables.product_country import fixup_product_countries_for_products


async def create_table(transaction):
    await transaction.execute(
        'create table "product_scans_by_country" ("product_id" int not null, "year" smallint not null, "country_id" int not null, "unique_scans" int not null, constraint "product_scans_by_country_pkey" primary key ("product_id", "year", "country_id"));',
    )
    await transaction.execute(
        'alter table "product_scans_by_country" add constraint "product_scans_by_country_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
    await transaction.execute(
        'alter table "product_scans_by_country" add constraint "product_scans_by_country_country_id_foreign" foreign key ("country_id") references "country" ("id") on update cascade on delete cascade;',
    )


async def create_scan(transaction, product, country, year, unique_scans):
    """This is only currently used in tests"""
    scan = await create_record(
        transaction,
        "product_scans_by_country",
        product_id=product["id"],
        country_id=country["id"],
        year=year,
        unique_scans=unique_scans,
    )
    await fixup_product_countries_for_products(transaction, [product["id"]])
    return scan


async def create_scans(transaction, scans: ProductScans):
    scans_by_country = []
    for code, years in scans.root.items():
        for year, scan_counts in years.root.items():
            for country, count in scan_counts.unique_scans_n_by_country.root.items():
                # For some reason the combination of execute many and using a values source in the SQL
                # converts everything to text, so need to supply text here and cast as int in the SQL
                scans_by_country.append([code, str(year), country, str(count)])

    if scans_by_country:
        # As mentioned above, need to cast ints in the SQL because of the source values clause
        await transaction.executemany(
            """insert into product_scans_by_country (product_id, year, country_id, unique_scans) 
            select product.id, source.year::numeric, country.id, source.scans::numeric 
            from (values ($1, $2, $3, $4)) as source (code, year, country, scans)
            join product on product.code = source.code
            join country on country.code = source.country
            on conflict (product_id, year, country_id) 
            do update set unique_scans = excluded.unique_scans""",
            scans_by_country,
        )
