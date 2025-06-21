"""Full list of nutrient tags that appear on actual products"""

from ..database import create_record, get_rows_affected


async def create_table(transaction):
    await transaction.execute(
        'create table "nutrient" ("id" serial primary key, "tag" text not null);',
    )
    await transaction.execute(
        'alter table "nutrient" add constraint "nutrient_tag_unique" unique ("tag");',
    )


async def create_nutrients_from_staging(transaction):
    return get_rows_affected(
        await transaction.execute(
            f"""insert into nutrient (tag)
        select distinct left(new_tag, -5)
        from product_temp pt
        cross join jsonb_object_keys(data->'nutriments') new_tag
        where right(new_tag, 5) = '_100g'
        and right(new_tag, 13) != 'prepared_100g'
        and not exists (select * from nutrient where tag = left(new_tag, -5))
        on conflict (tag) 
        do nothing
        """
        )
    )


async def create_nutrient(transaction, **params):
    return await create_record(transaction, "nutrient", **params)


async def get_nutrient(transaction, tag):
    return await transaction.fetchrow("select * from nutrient where tag = $1", tag)
