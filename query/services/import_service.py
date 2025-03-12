from typing import Dict

from query.database import database_connection
from query.models.product import Product
from query.mongodb import find_products
from query.tables.product_tags import tag_tables
from query.tables.product import create_product, product_fields

async def import_with_filter(filter: Dict):
    async with database_connection() as connection:
        projection = {key: True for key in (list(tag_tables.keys()) + list(product_fields.keys()))}
        async with find_products(filter, projection) as cursor:
            async for product in cursor:
                await create_product(connection, Product(code=product['code']))