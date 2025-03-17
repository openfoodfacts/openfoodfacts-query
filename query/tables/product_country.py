from query.models.country import Country
from query.models.product import Product


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


async def create_product_country(
    connection, product: Product, country: Country, recent_scans, total_scans
):
    await connection.execute(
        "INSERT INTO product_country (product_id, country_id, recent_scans, total_scans) VALUES ($1, $2, $3, $4)",
        product.id,
        country.id,
        recent_scans,
        total_scans,
    )


async def get_product_countries(connection, product_id):
    return await connection.fetch(
        "SELECT * FROM product_country WHERE product_id = $1", product_id
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
