from unittest.mock import patch
from query.database import database_connection
from query.models.country import Country
from query.models.query import Filter, FindQuery
from query.models.scans_by_country import ScansByCountry
from query.services import query
from query.services.query_count_test import create_test_tags
from query.tables.country import create_country
from query.tables.product_scans_by_country import create_scans
from query.test_helper import mock_cursor, random_code


@patch("query.services.query.find_products")
async def test_sorts_by_world_scans(mocked_mongo):
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
        mocked_mongo.return_value.__aenter__.return_value = mock_cursor(
            [
                {"code": tags.product1.code},
                {"code": tags.product2.code},
                {"code": tags.product3.code},
            ]
        )

        country = Country(tag=random_code(), code=random_code())
        await create_country(connection, country)
        await create_scans(
            connection,
            [
                ScansByCountry(
                    product=tags.product1, country=country, year=2024, unique_scans=10
                ),
                ScansByCountry(
                    product=tags.product2, country=country, year=2024, unique_scans=100
                ),
                ScansByCountry(
                    product=tags.product3, country=country, year=2024, unique_scans=100
                ),
                ScansByCountry(
                    product=tags.product3, country=country, year=2023, unique_scans=1
                ),
            ],
        )

        results = await query.find(
            FindQuery(
                filter=Filter(countries_tags=country.tag),
                projection={"code": True},
                sort=[("popularity_key", -1)],
            )
        )
        assert mocked_mongo.called
        call_args = mocked_mongo.call_args
        assert len(call_args[0][0]["_id"]) == 3
        product1_index = [i for i, result in enumerate(results) if result['code'] == tags.product1.code][0]
        product2_index = [i for i, result in enumerate(results) if result['code'] == tags.product2.code][0]
        product3_index = [i for i, result in enumerate(results) if result['code'] == tags.product3.code][0]
        assert product2_index < product1_index
        assert product3_index < product2_index
