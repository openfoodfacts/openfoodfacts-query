from uuid import uuid4
from query.db import Database
from query.models.product import Product
from query.tables.product import create_product
from query.test_helper import random_code


async def test_create_product():
    async with Database() as connection:
        id = await create_product(connection, Product(code = random_code()))
        assert id > 0