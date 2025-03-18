from query.database import database_connection
from query.tables.product import create_product
from query.test_helper import random_code


async def test_create_product():
    async with database_connection() as connection:
        product = await create_product(connection, code = random_code())
        assert product['id'] > 0