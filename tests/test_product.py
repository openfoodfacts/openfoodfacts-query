from uuid import uuid4
from query.db import Database
from query.tables.product import create_product
from tests.helper import random_code


async def test_create_product():
    async with Database() as connection:
        id = await create_product(connection, random_code())
        assert id > 0