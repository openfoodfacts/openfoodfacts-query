import datetime
from typing import Dict

from query.database import database_connection
from query.models.product import Product, Source
from query.mongodb import find_products
from query.tables.loaded_tag import append_loaded_tags
from query.tables.product_country import fixup_product_countries
from query.tables.product_tags import create_tags, delete_tags_not_in_this_load, tag_tables
from query.tables.product import create_product, delete_products_not_in_this_load, product_fields


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
                        last_processed=datetime.datetime.now(datetime.timezone.utc),
                        revision=product_data.get("rev"),
                    ),
                )
                await create_tags(connection, product, product_data)
                await fixup_product_countries(connection, product)

        # TODO: Only on full load
        await delete_products_not_in_this_load(connection, process_id)
        await delete_tags_not_in_this_load(connection, process_id)
        await append_loaded_tags(connection, tag_tables.keys())

async def import_from_mongo():
    await import_with_filter({}, Source.full_load)
