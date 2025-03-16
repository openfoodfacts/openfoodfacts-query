from datetime import datetime, timezone
from asyncpg import Connection, Record

from query.models.product import Product, Source
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


async def update_product(connection: Connection, product: Product):
    await connection.execute(
        "UPDATE product SET creator=$2, obsolete=$3, process_id=$4, source=$5, last_processed=$6, revision = $7, last_updated = $8 WHERE id = $1",
        product.id,
        product.creator,
        product.obsolete,
        product.process_id,
        product.source,
        product.last_processed,
        product.revision,
        product.last_updated,
    )
    return product


async def create_product(connection: Connection, product: Product):
    product.id = await connection.fetchval(
        "INSERT INTO product (code, creator, obsolete, process_id, source, last_processed, revision, last_updated) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id",
        product.code,
        product.creator,
        product.obsolete,
        product.process_id,
        product.source,
        product.last_processed,
        product.revision,
        product.last_updated,
    )
    return product


async def get_product(connection: Connection, code):
    return await connection.fetchrow("SELECT * FROM product WHERE code = $1", code)


async def delete_products(connection, process_id, source, codes = None):
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
        *args
    )
    deleted_ids = [result["id"] for result in results]
    await delete_tags(connection, deleted_ids)
    await delete_ingredients(connection, deleted_ids)
