"""Full list of nutrient tags that appear on actual products"""

from ..database import create_record


async def create_table(transaction):
    await transaction.execute(
        'create table "nutrient" ("id" serial primary key, "tag" text not null);',
    )
    await transaction.execute(
        'alter table "nutrient" add constraint "nutrient_tag_unique" unique ("tag");',
    )


async def create_nutrient(transaction, **params):
    return await create_record(transaction, "nutrient", **params)


async def get_nutrient(transaction, tag):
    return await transaction.fetchrow("select * from nutrient where tag = $1", tag)
