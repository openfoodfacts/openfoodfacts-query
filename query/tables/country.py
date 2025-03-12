from typing import List

from query.models.country import Country


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


async def create_country(connection, country: Country):
    country.id = await connection.fetchval(
        """INSERT INTO country (tag, code)
            VALUES ($1, $2) RETURNING id""",
        country.tag, country.code
    )
    return country


async def create_missing_countries(connection, countries: List[Country]):
    await connection.executemany(
        """INSERT INTO country (tag, code)
            SELECT $1, $2 WHERE NOT EXISTS
                (SELECT * FROM country WHERE tag = $1 AND COALESCE(code, '') = COALESCE($2, '')
            ON CONFLICT (tag) 
            DO UPDATE SET code = EXCLUDED.code""",
        {[c.tag, c.code] for c in countries}
    )

async def get_country(connection, tag):
    result = await connection.fetchrow(
        """SELECT id, tag, code FROM country WHERE tag = $1""",
       tag
    )
    return Country(result['tag'], result['code'], result['id'])
