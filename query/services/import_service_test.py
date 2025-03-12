from unittest.mock import patch
from query.database import database_connection
from query.services.import_service import import_with_filter
from query.test_helper import mock_cursor, random_code


@patch("query.services.import_service.find_products")
async def test_imports_product_by_code(mocked_mongo):
    product_code = random_code()

    mocked_mongo.return_value.__aenter__.return_value = mock_cursor(
        [
            {"code": product_code},
        ]
    )
    await import_with_filter({"_id": {"$in": [product_code]}})
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 1
    async with database_connection() as conn:
        product = await conn.fetchrow("SELECT * FROM product WHERE code = $1", product_code)
        assert product['code'] == product_code
