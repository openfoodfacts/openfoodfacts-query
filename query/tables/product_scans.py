"""The Number of scans for each product by year"""

from query.database import create_record
from ..models.scan import ProductScans


async def create_product_scans_table(transaction):
    await transaction.execute(
        'create table "product_scans" ("product_id" int not null, "year" smallint not null, "scan_count" int not null, "unique_scan_count" int not null, constraint "product_scans_pkey" primary key ("product_id", "year"));',
    )
    await transaction.execute(
        'alter table "product_scans" add constraint "product_scans_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )


async def insert_product_scans(transaction, scans: ProductScans):
    scans_by_product = []
    for code, years in scans.root.items():
        for year, scan_counts in years.root.items():
            # For some reason the combination of execute many and using a values source in the SQL
            # converts everything to text, so need to supply text here and cast as int in the SQL
            scans_by_product.append([code, str(year), str(scan_counts.scans_n), str(scan_counts.unique_scans_n)])

    if scans_by_product:
        # As mentioned above, need to cast ints in the SQL because of the source values clause
        await transaction.executemany(
            """insert into product_scans (product_id, year, scan_count, unique_scan_count) 
            select product.id, source.year::numeric, source.scans::numeric, source.unique_scans::numeric
            from (values ($1, $2, $3, $4)) as source (code, year, scans, unique_scans)
            join product on product.code = source.code
            on conflict (product_id, year) 
            do update set scan_count = excluded.scan_count, unique_scan_count = excluded.unique_scan_count""",
            scans_by_product,
        )


async def create_product_scan(transaction, product, year, scan_count, unique_scan_count):
    """This is only currently used in tests"""
    scan = await create_record(
        transaction,
        "product_scans",
        product_id=product["id"],
        year=year,
        scan_count=scan_count,
        unique_scan_count=unique_scan_count,
    )
    return scan

