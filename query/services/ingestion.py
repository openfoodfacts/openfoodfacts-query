from datetime import datetime, timezone
import logging
import math
from typing import Dict

from query.database import database_connection
from query.models.product import Product, Source
from query.mongodb import find_products
from query.tables.loaded_tag import append_loaded_tags, get_loaded_tags
from query.tables.product_country import fixup_product_countries
from query.tables.product_ingredient import create_ingredients
from query.tables.product_tags import create_tags, tag_tables
from query.tables.product import (
    create_product,
    delete_products,
    get_product,
    product_fields,
    update_product,
)
from query.tables.settings import get_last_updated, set_last_updated


logger = logging.getLogger(__name__)


async def get_process_id(connection):
    return await connection.fetchval("SELECT pg_current_xact_id()")


min_datetime = datetime(1, 1, 1, tzinfo=timezone.utc)


async def import_with_filter(filter: Dict, source: Source) -> datetime:
    max_last_updated = min_datetime
    found_product_codes = []
    async with database_connection() as connection:
        process_id = await get_process_id(connection)
        projection = {
            key: True for key in (list(tag_tables.keys()) + list(product_fields.keys()))
        }
        async with find_products(filter, projection) as cursor:
            async for product_data in cursor:
                # Fall back to last_modified_t if last_updated_t is not available
                try:
                    last_updated = datetime.fromtimestamp(
                        product_data.get(
                            "last_updated_t", product_data.get("last_modified_t")
                        ),
                        timezone.utc,
                    )
                except TypeError:
                    logger.warning(
                        f"Product: {product_data['code']}. Invalid last_updated_t: {product_data.get('last_updated_t')}, or last_modified_t: {product_data.get('last_modified_t')}."
                    )
                    last_updated = min_datetime
                product_code = product_data["code"]
                found_product_codes.append(product_code)
                existing_product = await get_product(connection, product_code)
                if (
                    existing_product
                    and source != Source.event
                    and existing_product["last_updated"] == last_updated
                ):
                    continue
                product = Product(
                    code=product_data["code"],
                    process_id=process_id,
                    source=source,
                    last_processed=datetime.now(timezone.utc),
                    last_updated=last_updated,
                    revision=product_data.get("rev"),
                )
                if existing_product:
                    product.id = existing_product["id"]
                    await update_product(connection, product)
                else:
                    await create_product(connection, product)
                await create_tags(connection, product, product_data)
                await fixup_product_countries(connection, product)
                await create_ingredients(
                    connection, product, product_data.get("ingredients", [])
                )
                max_last_updated = max(last_updated, max_last_updated)

        # Mark all products specifically requested but not found as deleted
        if source != Source.full_load and "code" in filter and "$in" in filter["code"]:
            requested_product_codes = filter["code"]["$in"]
            missing_product_codes = [
                code
                for code in requested_product_codes
                if code not in found_product_codes
            ]
            await delete_products(connection, process_id, source, missing_product_codes)

        if source == Source.full_load:
            await delete_products(connection, process_id, source)
            await append_loaded_tags(connection, tag_tables.keys())

    return max_last_updated


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
