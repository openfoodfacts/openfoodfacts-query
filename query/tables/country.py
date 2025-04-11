"""Full list of countries. Will include the countries taxonomy plus other country values that have appeared in scans or product countries_tags"""

import json
import os

from asyncpg import Connection

from query.database import create_record


async def create_table(transaction):
    await transaction.execute(
        'create table "country" ("id" serial primary key, "code" text null, "tag" text not null);',
    )
    await transaction.execute(
        'alter table "country" add constraint "country_code_unique" unique ("code");',
    )
    await transaction.execute(
        'alter table "country" add constraint "country_tag_unique" unique ("tag");',
    )
    # insert world countries for tests.
    await transaction.execute(
        """insert into country (code, tag) values ('world','en:world')"""
    )
    # create countries from existing data
    await transaction.execute(
        """insert into country (tag)
        select distinct pct.value
        from product_countries_tag pct
        where not exists (select * from country where tag = pct.value)
        on conflict (tag) do nothing"""
    )


async def create_country(transaction, **params):
    return await create_record(transaction, "country", **params)


async def get_country(transaction, tag):
    return await transaction.fetchrow("select * from country where tag = $1", tag)


def lower_or_none(value):
    return None if value == None else value.lower()


with open(f"{os.path.dirname(__file__)}/../assets/countries.json") as f:
    countries = json.load(f)


def country_data():
    return [
        [country_id, lower_or_none(country.get("country_code_2", {}).get("en"))]
        for country_id, country in countries.items()
    ]


def country_codes():
    return [country[1] for country in country_data() if country[1]]


async def add_all_countries(transaction: Connection):
    await transaction.executemany(
        """insert into country (tag, code) select tag, code 
        from (values ($1, $2)) as source (tag, code)
        where not exists (select * from country where tag = source.tag and code = source.code)
        on conflict (tag) 
        do update set code = excluded.code""",
        country_data(),
    )
