from datetime import datetime, timezone
from asyncpg import Connection

from query.database import create_record, database_connection, get_rows_affected
from query.models.product import Source
from query.tables.product_ingredient import delete_ingredients
from query.tables.product_tags import delete_tags

product_fields = {
    "code": "code",
    "product_name": "name",
    "creator": "creator",
    "owners_tags": "owners_tags",
    "last_modified_t": None,  # Note we actually use last_updated_t for checks but not all products may have this
    "last_updated_t": "last_updated",
    "ingredients_n": "ingredients_count",
    "ingredients_without_ciqual_codes_n": "ingredients_without_ciqual_codes_count",
    "ingredients": None,
    "rev": "revision",
}


def product_filter_fields():
    return [key for key, value in product_fields.items() if value]


product_columns = [value for value in product_fields.values() if value]


async def create_table(connection: Connection):
    await connection.execute(
        """create table product (
            id serial not null,
            name text null,
            code text null,
            last_updated timestamptz null,
            creator text null,
            owners_tags text null,
            obsolete boolean null default false,
            ingredients_without_ciqual_codes_count int null,
            ingredients_count int null,
            last_processed timestamptz null,
            source varchar(255) null,
            revision int null,
            process_id bigint null,
            constraint product_pkey primary key (id));""",
    )
    await connection.execute(
        "create index product_code_index on product (code);",
    )
    await connection.execute(
        "create index product_process_id_index on product (process_id);"
    )
    await connection.execute("create index product_creator_index on product (creator);")
    await connection.execute(
        "create index product_owners_tags_index on product (owners_tags);"
    )


async def update_products_from_staging(
    connection: Connection, log, obsolete, process_id, source
):
    # Apply updates to products
    product_results = await connection.execute(
        f"""
      update product
      set name = tp.data->>'product_name',
        creator = tp.data->>'creator',
        owners_tags = tp.data->>'owners_tags',
        obsolete = $1,
        ingredients_count = (tp.data->>'ingredients_n')::numeric,
        ingredients_without_ciqual_codes_count = (tp.data->>'ingredients_without_ciqual_codes_n')::numeric,
        last_updated = tp.last_updated,
        process_id = $2,
        last_processed = $3,
        source = $4,
        revision = (tp.data->>'rev')::int
      from product_temp tp
      where product.id = tp.id""",
        obsolete,
        process_id,
        datetime.now(timezone.utc),
        source,
    )
    log(f"Updated {get_rows_affected(product_results)} products")


async def get_minimal_product(connection, code):
    return await connection.fetchrow(
        "SELECT id, last_updated FROM product WHERE code = $1", code
    )


async def create_minimal_product(connection, code):
    return await connection.fetchrow(
        "INSERT INTO product (code) VALUES ($1) RETURNING id", code
    )


async def create_product(connection, **params):
    return await create_record(connection, "product", **params)


async def get_product(connection: Connection, code):
    return await connection.fetchrow("SELECT * FROM product WHERE code = $1", code)


async def get_product_by_id(id):
    async with database_connection() as connection:
        return await connection.fetchrow("SELECT * FROM product WHERE id = $1", id)


async def delete_products(connection, process_id, source, codes=None):
    args = [process_id, datetime.now(timezone.utc), source]
    if codes:
        args.append(codes)
    results = await connection.fetch(
        f"""UPDATE product SET 
                obsolete = NULL,
                process_id = $1,
                last_processed = $2,
                source = $3 
            WHERE obsolete IS NOT NULL
                {"AND process_id < $1" if source == Source.full_load else ""}
                {"AND code = ANY($4)" if codes else ""}
            RETURNING id""",
        *args,
    )
    deleted_ids = [result["id"] for result in results]
    await delete_tags(connection, deleted_ids)
    await delete_ingredients(connection, deleted_ids)
