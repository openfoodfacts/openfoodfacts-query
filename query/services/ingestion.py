from datetime import datetime, timezone
import logging
import math
from typing import Dict

from query.database import database_connection
from query.models.product import Product, Source
from query.mongodb import find_products
from query.tables.loaded_tag import append_loaded_tags
from query.tables.product_country import fixup_product_countries
from query.tables.product_tags import create_tags, delete_tags_not_in_this_load, tag_tables
from query.tables.product import create_product, delete_products_not_in_this_load, product_fields
from query.tables.settings import get_last_updated


logger = logging.getLogger(__name__)

async def get_process_id(connection):
    return await connection.fetchval("SELECT pg_current_xact_id()")


async def import_with_filter(filter: Dict, source: Source):
    async with database_connection() as connection:
        process_id = await get_process_id(connection)
        projection = {
            key: True for key in (list(tag_tables.keys()) + list(product_fields.keys()))
        }
        async with find_products(filter, projection) as cursor:
            async for product_data in cursor:
                product = await create_product(
                    connection,
                    Product(
                        code=product_data["code"],
                        process_id=process_id,
                        source=source,
                        last_processed=datetime.now(timezone.utc),
                        revision=product_data.get("rev"),
                    ),
                )
                await create_tags(connection, product, product_data)
                await fixup_product_countries(connection, product)

        if source == Source.full_load:
            await delete_products_not_in_this_load(connection, process_id)
            await delete_tags_not_in_this_load(connection, process_id)
            await append_loaded_tags(connection, tag_tables.keys())


async def import_from_mongo(from_date: str = None):
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
            from_time = math.floor(datetime.fromisoformat(from_date).timestamp() / 1000)
            filter['last_updated_t'] = { "$gt": from_time }
            logger.info(f"Starting import from {from_date}")

        await import_with_filter(filter, source)
