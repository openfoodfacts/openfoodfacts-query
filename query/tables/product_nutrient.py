"""This will contain a record for each nutrient on a product"""

from asyncpg import Connection
from query.tables.loaded_tag import PARTIAL_TAGS
from ..database import create_record, get_rows_affected

NUTRIENT_TAG = "nutriments"


async def create_table(transaction):
    await transaction.execute(
        'create table "product_nutrient" ("product_id" int not null, "obsolete" boolean null, "nutrient_id" int not null, "value" double precision not null, primary key ("product_id", "nutrient_id"));',
    )
    await transaction.execute(
        'alter table "product_nutrient" add constraint "product_nutrient_product_id_foreign" foreign key ("product_id") references "product" ("id") on update cascade on delete cascade;',
    )
    await transaction.execute(
        'alter table "product_nutrient" add constraint "product_nutrient_nutrient_id_foreign" foreign key ("nutrient_id") references "nutrient" ("id") on update cascade on delete cascade;',
    )
    # Index for fast searches
    await transaction.execute(
        "create index product_nutrient_ix1 on product_nutrient (nutrient_id, value, product_id);",
    )


async def create_product_nutrient(
    transaction, product, nutrient, value
):
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


async def create_nutrients_from_staging(transaction: Connection, log, obsolete):
    deleted = await transaction.execute(
        """delete from product_nutrient 
        where product_id in (select id from product_temp)"""
    )
    log_text = f"Updated nutrients deleted {get_rows_affected(deleted)},"
    
    # Create any missing nutrient types
    nutrients_added = get_rows_affected(await transaction.execute(
        f"""insert into nutrient (tag)
        select distinct left(new_tag, -5)
        from product_temp pt
        cross join jsonb_object_keys(data->'nutriments') new_tag
        where right(new_tag, 5) = '_100g'
        and not exists (select * from nutrient where tag = left(new_tag, -5))
        on conflict (tag) 
        do nothing"""))
    if nutrients_added:
        log_text += f" added {nutrients_added} nutrient tags, "
    
    product_nutrients_added = get_rows_affected(await transaction.execute(
        f"""insert into product_nutrient (product_id, nutrient_id, value)
        select distinct pt.id, n.id, source.value::double precision
        from product_temp pt
        cross join jsonb_each(data->'nutriments') source
        join nutrient n on n.tag = left(source.key, -5)
        where right(source.key, 5) = '_100g'"""))
    log_text += f" added {product_nutrients_added} product nutrients"
    log(log_text)


async def delete_product_nutrient(transaction, product_ids):
    """Soft delete by setting the obsolete flag to null"""
    await transaction.execute(
        f"UPDATE product_nutrient SET obsolete = NULL WHERE product_id = ANY($1::numeric[])",
        product_ids,
    )
