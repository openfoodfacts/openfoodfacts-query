from query.database import create_record, database_connection


async def create_table(connection):
    await connection.execute(
        'create table "product_country" ("product_id" int not null, "obsolete" boolean null, "country_id" int not null, "recent_scans" int not null, "total_scans" int not null, constraint "product_country_pkey" primary key ("product_id", "country_id"));',
    )
    await connection.execute(
        'alter table "product_country" add constraint "product_country_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
    await connection.execute(
        'alter table "product_country" add constraint "product_country_country_id_foreign" foreign key ("country_id") references "country" ("id") on update cascade on delete cascade;',
    )
    # Create product country entries for existing products
    await connection.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT pct.product_id, pct.obsolete, c.id, 0, 0
        FROM product_countries_tag pct
        JOIN country c ON c.tag = pct.value
        ON CONFLICT (product_id, country_id) DO NOTHING"""
    )
    # Create world entries for existing products
    await connection.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT p.id, p.obsolete, c.id, 0, 0
        FROM product p, country c
        WHERE c.tag = 'en:world'
        ON CONFLICT (product_id, country_id) DO NOTHING"""
    )
    await connection.execute(
        "create index product_country_ix1 on product_country (obsolete, country_id, recent_scans DESC, total_scans DESC, product_id);",
    )


async def create_product_country(connection, product, country, recent_scans, total_scans):
    return await create_record(connection, "product_country", product_id=product['id'], country_id=country['id'], recent_scans=recent_scans, total_scans=total_scans)


async def get_product_countries(connection, product):
    return await connection.fetch(
        "SELECT * FROM product_country WHERE product_id = $1", product['id']
    )


async def fixup_product_countries(connection, obsolete):
    # Create missing countries
    await connection.execute(
        """INSERT INTO country (tag) SELECT DISTINCT pct.value 
            FROM product_temp pt
            JOIN product_countries_tag pct ON pct.product_id = pt.id
            WHERE NOT EXISTS (SELECT * FROM country WHERE tag = pct.value)
            ON CONFLICT (tag) DO NOTHING""")
    await connection.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
            SELECT pct.product_id, $1, c.id, 0, 0
            FROM (SELECT product_id, value FROM product_temp JOIN product_countries_tag ON product_id = id
                UNION SELECT id, 'en:world' FROM product_temp) pct
            JOIN country c ON c.tag = pct.value
            ON CONFLICT (product_id, country_id) DO NOTHING""", obsolete
    )


async def fixup_product_countries_for_product(connection, product_id):
    await connection.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT product_id, p.obsolete, country_id, unique_scans, unique_scans
        FROM product_scans_by_country
        JOIN product p ON p.id = product_id
        WHERE product_id = $1
        AND year = $2
        ON CONFLICT (product_id, country_id)
        DO UPDATE SET recent_scans = EXCLUDED.recent_scans, obsolete = EXCLUDED.obsolete""",
        product_id, 2024)

    await connection.execute(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT product_id, p.obsolete, country_id, 0, sum(unique_scans)
        FROM product_scans_by_country
        JOIN product p ON p.id = product_id
        WHERE product_id = $1
        AND year >= $2
        GROUP BY product_id, p.obsolete, country_id
        ON CONFLICT (product_id, country_id)
        DO UPDATE SET total_scans = EXCLUDED.total_scans, obsolete = EXCLUDED.obsolete""",
        product_id, 2019,
    )
        
