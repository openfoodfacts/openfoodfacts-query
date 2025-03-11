from uuid import uuid4
from query.database import database_connection
from query.models.product import Product
from query.tables.product import create_product
from query.test_helper import random_code


async def test_create_product():
    async with database_connection() as connection:
        id = await create_product(connection, Product(code = random_code()))
        assert id > 0