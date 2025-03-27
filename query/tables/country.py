import json
import os

from asyncpg import Connection

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
    # insert world countries for tests.
    await connection.execute(
        """insert into country (code, tag) values ('world','en:world')"""
    )
    # create countries from existing data
    await connection.execute(
        """insert into country (tag)
        select distinct pct.value
        from product_countries_tag pct
        where not exists (select * from country where tag = pct.value)
        on conflict (tag) do nothing"""
    )


async def create_country(connection, **params):
    return await create_record(connection, "country", **params)


async def get_country(connection, tag):
    return await connection.fetchrow("select * from country where tag = $1", tag)


def lower_or_none(value):
    return None if value == None else value.lower()

async def add_all_countries(connection: Connection):
    with open(f"{os.path.dirname(__file__)}/../assets/countries.json") as f:
        countries = json.load(f)
    
    country_codes = [[country_id, lower_or_none(country.get('country_code_2', {}).get('en'))] for country_id, country in countries.items()]

    await connection.executemany("""insert into country (tag, code) select tag, code 
        from (values ($1, $2)) as source (tag, code)
        where not exists (select * from country where tag = source.tag and code = source.code)
        on conflict (tag) 
        do update set code = excluded.code""", country_codes)