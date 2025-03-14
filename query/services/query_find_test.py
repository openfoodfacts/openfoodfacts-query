from unittest.mock import patch
from query.database import database_connection
from query.models.query import Filter, FindQuery
from query.models.scans_by_country import ScansByCountry
from query.services import query
from query.services.query_count_test import create_test_tags
from query.tables.country import get_country
from query.tables.product_scans_by_country import create_scans
from query.test_helper import mock_cursor, patch_context_manager


@patch("query.services.query.find_products")
async def test_sorts_by_country_scans(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(mocked_mongo, mock_cursor(
        [
            {"code": tags.product1.code},
            {"code": tags.product2.code},
            {"code": tags.product3.code},
        ]
    ))
    results = await query.find(
        FindQuery(
            filter=Filter(countries_tags=tags.country.tag),
            projection={"code": True},
            sort=[("popularity_key", -1)],
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 3
    assert results[0]["code"] == tags.product3.code
    assert results[1]["code"] == tags.product2.code
    assert results[2]["code"] == tags.product1.code


@patch("query.services.query.find_products")
async def test_sorts_by_world_scans(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(mocked_mongo, mock_cursor(
        [
            {"code": tags.product1.code},
            {"code": tags.product2.code},
            {"code": tags.product3.code},
        ]
    ))
    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True},
            sort=[("popularity_key", -1)],
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 3
    assert call_args[0][1] == {"code": True}
    assert len(results) == 3
    assert results[0]["code"] == tags.product2.code
    assert results[1]["code"] == tags.product3.code
    assert results[2]["code"] == tags.product1.code


@patch("query.services.query.find_products")
async def test_limit_and_offset(mocked_mongo):
    tags = await create_tags_and_scans()

    # Using world so order should be 2,3,1 but skipping 2 and limiting to 1
    patch_context_manager(mocked_mongo, mock_cursor(
        [
            {"code": tags.product3.code},
        ]
    ))
    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True},
            sort=[("popularity_key", -1)],
            skip=1,
            limit=1,
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 1
    assert call_args[0][1] == {"code": True}
    assert len(results) == 1
    assert results[0]["code"] == tags.product3.code


@patch("query.services.query.find_products")
async def test_obsolete(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(mocked_mongo, mock_cursor(
        [
            {"code": tags.product4.code},
        ]
    ))
    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True},
            sort=[("popularity_key", -1)],
        ),
        True,
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 1
    assert call_args[0][2] == True
    assert len(results) == 1
    assert results[0]["code"] == tags.product4.code


async def create_tags_and_scans():
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
        world = await get_country(connection, "en:world")
        # Country sequence should be: 3,2,1. World sequence: 2,3,1
        await create_scans(
            connection,
            [
                ScansByCountry(tags.product1, tags.country, 2024, 10),
                ScansByCountry(tags.product2, tags.country, 2024, 100),
                ScansByCountry(tags.product3, tags.country, 2024, 100),
                ScansByCountry(tags.product3, tags.country, 2023, 1),
                ScansByCountry(tags.product4, tags.country, 2024, 50),
                ScansByCountry(tags.product1, world, 2024, 20),
                ScansByCountry(tags.product2, world, 2024, 201),
                ScansByCountry(tags.product3, world, 2024, 200),
                ScansByCountry(tags.product3, world, 2023, 100),
                ScansByCountry(tags.product4, world, 2024, 50),
            ],
        )

        return tags
