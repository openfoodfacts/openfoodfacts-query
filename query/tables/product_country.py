from query.database import create_record

OLDEST_YEAR = 2019
CURRENT_YEAR = 2024
PRODUCT_COUNTRY_TAG = "product_country"


async def create_table(transaction):
    await transaction.execute(
        'create table "product_country" ("product_id" int not null, "obsolete" boolean null, "country_id" int not null, "recent_scans" int not null, "total_scans" int not null, constraint "product_country_pkey" primary key ("product_id", "country_id"));',
    )
    await transaction.execute(
        'alter table "product_country" add constraint "product_country_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
    await transaction.execute(
        'alter table "product_country" add constraint "product_country_country_id_foreign" foreign key ("country_id") references "country" ("id") on update cascade on delete cascade;',
    )
    # Create product country entries for existing products
    await transaction.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT pct.product_id, pct.obsolete, c.id, 0, 0
        FROM product_countries_tag pct
        JOIN country c ON c.tag = pct.value
        ON CONFLICT (product_id, country_id) DO NOTHING"""
    )
    # Create world entries for existing products
    await transaction.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT p.id, p.obsolete, c.id, 0, 0
        FROM product p, country c
        WHERE c.tag = 'en:world'
        ON CONFLICT (product_id, country_id) DO NOTHING"""
    )
    await transaction.execute(
        "create index product_country_ix1 on product_country (obsolete, country_id, recent_scans DESC, total_scans DESC, product_id);",
    )


async def fix_index(transaction):
    """Change column order so it is quicker to delete rogue countries"""
    await transaction.execute("drop index product_country_ix1")
    await transaction.execute(
        "create index product_country_ix1 on product_country (country_id, obsolete, recent_scans DESC, total_scans DESC, product_id);",
    )


async def create_product_country(
    transaction, product, country, recent_scans, total_scans
):
    return await create_record(
        transaction,
        "product_country",
        product_id=product["id"],
        country_id=country["id"],
        recent_scans=recent_scans,
        total_scans=total_scans,
    )


async def get_product_countries(transaction, product):
    return await transaction.fetch(
        "SELECT * FROM product_country WHERE product_id = $1", product["id"]
    )


async def fixup_product_countries(transaction, obsolete):
    # Create missing countries
    await transaction.execute(
        """INSERT INTO country (tag) SELECT DISTINCT pct.value 
            FROM product_temp pt
            JOIN product_countries_tag pct ON pct.product_id = pt.id
            WHERE NOT EXISTS (SELECT * FROM country WHERE tag = pct.value)
            ON CONFLICT (tag) DO NOTHING"""
    )
    await transaction.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
            SELECT pct.product_id, $1, c.id, 0, 0
            FROM (SELECT product_id, value FROM product_temp JOIN product_countries_tag ON product_id = id
                UNION SELECT id, 'en:world' FROM product_temp) pct
            JOIN country c ON c.tag = pct.value
            ON CONFLICT (product_id, country_id) DO NOTHING""",
        obsolete,
    )


async def fixup_product_countries_for_products(transaction, ids_updated):
    await transaction.execute(
        """insert into product_country (product_id, obsolete, country_id, recent_scans, total_scans)
            select product_id, p.obsolete, country_id, sum(CASE WHEN year = $3 THEN unique_scans ELSE 0 END), sum(CASE WHEN year >= $2 THEN unique_scans ELSE 0 END)
            from product_scans_by_country
            join product p on p.id = product_id
            where product_id = ANY($1)
            group by product_id, p.obsolete, country_id
            on conflict (product_id, country_id)
            do update set recent_scans = excluded.recent_scans, total_scans = excluded.total_scans, obsolete = excluded.obsolete""",
        ids_updated,
        OLDEST_YEAR,
        CURRENT_YEAR,
    )

    # Note that the product_counties_tag table and product_country table could potentially get of of sync a bit, but don't worry about this for now
