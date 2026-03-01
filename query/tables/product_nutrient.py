"""This will contain a record for each nutrient on a product"""

from asyncpg import Connection

from query.tables.nutrient import create_nutrients_from_staging

from ..database import create_record, get_rows_affected

NUTRIENT_TAG = "nutriments"
NUTRITION_TAG = "nutrition.aggregated_set.nutrients"


async def create_table(transaction):
    await transaction.execute(
        'create table "product_nutrient" ("product_id" int not null, "nutrient_id" int not null, "value" double precision not null, primary key ("product_id", "nutrient_id"));',
    )
    await transaction.execute(
        'alter table "product_nutrient" add constraint "product_nutrient_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
    await transaction.execute(
        'alter table "product_nutrient" add constraint "product_nutrient_nutrient_id_foreign" foreign key ("nutrient_id") references "nutrient" ("id") on update cascade on delete cascade;',
    )
    # Index for fast searches
    await transaction.execute(
        "create index product_nutrient_ix1 on product_nutrient (nutrient_id, value);",
    )


async def create_product_nutrient(transaction, product, nutrient, value):
    return await create_record(
        transaction,
        "product_nutrient",
        product_id=product["id"],
        nutrient_id=nutrient["id"],
        value=value,
    )


async def get_product_nutrients(transaction, product):
    return await transaction.fetch(
        "SELECT * FROM product_nutrient WHERE product_id = $1", product["id"]
    )


async def create_product_nutrients_from_staging(transaction: Connection, log):
    deleted = await transaction.execute(
        """delete from product_nutrient 
        where product_id in (select id from product_temp)"""
    )
    log_text = f"Updated nutrients deleted {get_rows_affected(deleted)},"

    # Create any missing nutrient types
    nutrients_added = await create_nutrients_from_staging(transaction)
    if nutrients_added:
        log_text += f" added {nutrients_added} nutrient tags,"

    product_nutrients_added = get_rows_affected(
        await transaction.execute(
            f"""insert into product_nutrient (product_id, nutrient_id, value)
        select pt.id, n.id, source.value::double precision
        from product_temp pt
        cross join jsonb_each(data->'nutriments') source
        join nutrient n on n.tag = left(source.key, -5)
        where right(source.key, 5) = '_100g'
        and right(source.key, 13) != 'prepared_100g'
        and pg_input_is_valid(source.value::text, 'double precision')
        union select pt.id, n.id, (source.value->'value')::double precision
        from product_temp pt
        cross join jsonb_each(data->'nutrition'->'aggregated_set'->'nutrients') source
        join nutrient n on n.tag = source.key
        where pg_input_is_valid(source.value->>'value', 'double precision')
        """
        )
    )
    log_text += f" added {product_nutrients_added} product nutrients"
    log(log_text)
