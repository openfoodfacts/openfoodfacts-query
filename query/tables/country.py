from typing import List

from query.database import create_record


async def create_table(connection):
    await connection.execute(
        'create table "country" ("id" serial primary key, "code" text null, "tag" text not null);',
    )
    await connection.execute(
        'alter table "country" add constraint "country_code_unique" unique ("code");',
    )
    await connection.execute(
        'alter table "country" add constraint "country_tag_unique" unique ("tag");',
    )
    # Insert world countries for tests.
    await connection.execute(
        """INSERT INTO country (code, tag) VALUES ('world','en:world')"""
    )
    # Create countries from existing data
    await connection.execute(
        """INSERT INTO country (tag)
        SELECT DISTINCT pct.value
        FROM product_countries_tag pct
        WHERE NOT EXISTS (SELECT * FROM country WHERE tag = pct.value)
        ON CONFLICT (tag) DO NOTHING"""
    )


async def create_country(connection, **params):
    return await create_record(connection, "country", **params)


async def get_country(connection, tag):
    return await connection.fetchrow("SELECT * FROM country WHERE tag = $1",tag)
