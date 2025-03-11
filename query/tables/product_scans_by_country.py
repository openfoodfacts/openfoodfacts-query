from typing import List
from query.models.scans_by_country import ScansByCountry


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


async def create_scans(connection, scans: List[ScansByCountry]):
    await connection.executemany(
        """INSERT INTO product_scans_by_country (product_id, year, country_id, unique_scans) 
          SELECT product.id, source.year::int, country.id, source.scans::int 
          FROM (values ($1, $2, $3, $4)) as source (code, year, country, scans)
          JOIN product ON product.code = source.code
          JOIN country ON country.code = source.country
          ON CONFLICT (product_id, year, country_id) 
          DO UPDATE SET unique_scans = EXCLUDED.unique_scans""",
        # For some reason executemany doesn't like non-string arguments below
        [(scan.product.code, str(scan.year), scan.country.code, str(scan.unique_scans))
            for scan in scans],
    )

    codes_updated = set([scan.product.code for scan in scans])
    await connection.executemany(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT product_id, p.obsolete, country_id, unique_scans, unique_scans
        FROM product_scans_by_country
        JOIN product p ON p.id = product_id
        WHERE p.code = $1
        AND year = $2
        ON CONFLICT (product_id, country_id)
        DO UPDATE SET recent_scans = EXCLUDED.recent_scans, obsolete = EXCLUDED.obsolete""",
        [(code, 2024) for code in codes_updated],
    )

    await connection.executemany(
        """INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT product_id, p.obsolete, country_id, 0, sum(unique_scans)
        FROM product_scans_by_country
        JOIN product p ON p.id = product_id
        WHERE p.code = $1
        AND year >= $2
        GROUP BY product_id, p.obsolete, country_id
        ON CONFLICT (product_id, country_id)
        DO UPDATE SET total_scans = EXCLUDED.total_scans, obsolete = EXCLUDED.obsolete""",
        [(code, 2019) for code in codes_updated],
    )
