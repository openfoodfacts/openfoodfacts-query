from datetime import datetime, timezone
import logging
import math
from typing import Dict

from asyncpg import Connection

from query.database import database_connection, get_rows_affected
from query.models.product import Product, Source
from query.mongodb import find_products
from query.tables.loaded_tag import append_loaded_tags, get_loaded_tags
from query.tables.product_country import fixup_product_countries
from query.tables.product_ingredient import (
    create_ingredients,
    create_ingredients_from_staging,
)
from query.tables.product_tags import create_tags, create_tags_from_staging, tag_tables
from query.tables.product import (
    create_product,
    delete_products,
    get_product,
    product_fields,
    update_product,
)
from query.tables.settings import get_last_updated, set_last_updated


logger = logging.getLogger(__name__)
min_datetime = datetime(1, 1, 1, tzinfo=timezone.utc)
batch_size = 10000


async def get_process_id(connection):
    return await connection.fetchval("SELECT pg_current_xact_id()")


def int_or_none(value):
    return None if value == None else int(value)


async def import_with_filter(filter: Dict, source: Source) -> datetime:
    max_last_updated = min_datetime
    found_product_codes = []
    codes_specified = "code" in filter and "$in" in filter["code"]

    async with database_connection() as connection:
        await connection.execute(
            "CREATE TEMP TABLE product_temp (id int PRIMARY KEY, last_updated timestamptz, data jsonb)"
        )
        try:
            process_id = await get_process_id(connection)
            projection = {
                key: True
                for key in (list(tag_tables.keys()) + list(product_fields.keys()))
            }
            for obsolete in [False, True]:
                product_count = 0
                async with find_products(filter, projection, obsolete) as cursor:
                    async for product_data in cursor:
                        if product_count == 0:
                            logger.info("Fetched first product")
                        product_count += 1

                        # Fall back to last_modified_t if last_updated_t is not available
                        try:
                            last_updated = datetime.fromtimestamp(
                                product_data.get(
                                    "last_updated_t",
                                    product_data.get("last_modified_t"),
                                ),
                                timezone.utc,
                            )
                        except TypeError:
                            logger.warning(
                                f"Product: {product_data['code']}. Invalid last_updated_t: {product_data.get('last_updated_t')}, or last_modified_t: {product_data.get('last_modified_t')}."
                            )
                            last_updated = min_datetime
                        product_code = product_data["code"]
                        if codes_specified:
                            found_product_codes.append(product_code)

                        existing_product = await connection.fetchrow("SELECT id, last_updated FROM product WHERE code = $1", product_code)
                        if (
                            existing_product
                            and source == Source.incremental_load
                            and existing_product["last_updated"] == last_updated
                        ):
                            continue
                        if not existing_product:
                            existing_product = await connection.fetchrow("INSERT INTO product (code) VALUES ($1) RETURNING id", product_code)

                        # Strip any nulls from tag text
                        for tag in tag_tables.keys():
                            tag_data = product_data.get(tag, [])
                            for i, tag_value in enumerate(tag_data):
                                if "\0" in tag_value:
                                    logger.warning(
                                        f"Product: {product_code}. Nuls stripped from {tag} value: {tag_value}"
                                    )
                                    tag_data[i] = tag_value.replace("\0", "")
                        await connection.execute(
                            "INSERT INTO product_temp (id, last_updated, data) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
                            existing_product['id'],
                            last_updated,
                            product_data,
                        )
                        if not (product_count % batch_size):
                            await apply_staged_changes(
                                connection, obsolete, product_count, process_id, source
                            )

                        max_last_updated = max(last_updated, max_last_updated)

                if product_count % batch_size:
                    await apply_staged_changes(connection, obsolete, product_count, process_id, source)

            # Mark all products specifically requested but not found as deleted
            if codes_specified:
                requested_product_codes = filter["code"]["$in"]
                missing_product_codes = [
                    code
                    for code in requested_product_codes
                    if code not in found_product_codes
                ]
                await delete_products(
                    connection, process_id, source, missing_product_codes
                )

            if source == Source.full_load:
                await delete_products(connection, process_id, source)
                await append_loaded_tags(connection, tag_tables.keys())
        finally:
            await connection.execute("DROP TABLE product_temp")

    return max_last_updated


async def apply_staged_changes(connection: Connection, obsolete, product_count, process_id, source):
    await connection.execute("ANALYZE product_temp")
    # Apply updates to products
    product_results = await connection.execute(f"""
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
      where product.id = tp.id""", obsolete, process_id, datetime.now(timezone.utc), source)
    logger.info(f"Updated {get_rows_affected(product_results)} products")

    await create_ingredients_from_staging(connection, logger, obsolete)
    await create_tags_from_staging(connection, logger, obsolete)
    await fixup_product_countries(connection, obsolete)
    await connection.execute("TRUNCATE TABLE product_temp")
    logger.info(f"Imported {product_count}{' obsolete' if obsolete else ''} products")


import_running = False
async def import_from_mongo(from_date: str = None):
    global import_running
    if import_running:
        logger.warning("Skipping as import already running")
        return

    import_running = True
    try:
        source = Source.full_load if from_date == None else Source.incremental_load
        #   If the from parameter is supplied but it is empty then obtain the most
        #   recent modified time from the database and query MongoDB for products
        #   modified since then
        async with database_connection() as connection:
            if not from_date and source == Source.incremental_load:
                last_updated = await get_last_updated(connection)
                from_date = last_updated.isoformat()
            filter = {}
            if from_date:
                # Note in python the timestamp is in whole seconds (matches Perl)
                from_time = math.floor(datetime.fromisoformat(from_date).timestamp())
                filter["last_updated_t"] = {"$gt": from_time}
                logger.info(f"Starting import from {from_date}")

            max_last_updated = await import_with_filter(filter, source)
            if max_last_updated != min_datetime:
                await set_last_updated(connection, max_last_updated)
    finally:
        import_running = False


async def scheduled_import_from_mongo():
    async with database_connection() as connection:
        loaded_tags = await get_loaded_tags(connection)
        # If every tag is loaded then we do an incremental import. otherwise full
        if any(tag for tag in tag_tables.keys() if tag not in loaded_tags):
            await import_from_mongo()
        else:
            await import_from_mongo("")
