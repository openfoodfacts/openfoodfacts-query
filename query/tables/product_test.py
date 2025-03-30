from query.database import database_connection
from query.tables.product import create_product, normalize_code
from query.test_helper import random_code


async def test_create_product():
    async with database_connection() as connection:
        product = await create_product(connection, code=random_code())
        assert product["id"] > 0

def test_normalize_code():
    assert normalize_code('0000a') == '0000a'
    assert normalize_code('000000000000001') == '00000001'
    assert normalize_code('1234567890') == '0001234567890'
    assert normalize_code('12345678901234') == '12345678901234'
