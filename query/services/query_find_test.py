from unittest.mock import patch

import pytest
from fastapi import HTTPException, status
from pydantic import ValidationError

from query.services import scan
from query.services.scan import scans_fully_loaded
from query.tables.product_nutrient import NUTRIENT_TAG, NUTRITION_TAG
from query.tables.product_scans import create_product_scan

from ..database import get_transaction
from ..models.query import Filter, FindQuery, Fragment, Qualify, SortColumn
from ..services import query
from ..services.query_count_test import create_test_tags
from ..tables.country import get_country
from ..tables.product_scans_by_country import create_scan
from ..test_helper import mock_cursor, patch_context_manager
from . import query

TEST_YEAR = 1900


@patch.object(query, "find_products")
async def test_sorts_by_country_scans(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(
        mocked_mongo,
        mock_cursor(
            [
                {"code": tags.product1["code"]},
                {"code": tags.product2["code"]},
                {"code": tags.product3["code"]},
            ]
        ),
    )
    results = await query.find(
        FindQuery(
            filter=Filter(countries_tags=tags.country["tag"]),
            projection={"code": True, "product_name": True},
            sort=[("popularity_key", -1)],
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 3
    assert results[0]["code"] == tags.product3["code"]
    assert results[1]["code"] == tags.product2["code"]
    assert results[2]["code"] == tags.product1["code"]


@patch.object(query, "find_products")
async def test_sorts_by_world_scans(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(
        mocked_mongo,
        mock_cursor(
            [
                {"code": tags.product1["code"]},
                {"code": tags.product2["code"]},
                {"code": tags.product3["code"]},
            ]
        ),
    )
    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True, "product_name": True},
            sort=[("popularity_key", -1)],
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 3
    assert call_args[0][1] == {"code": True, "product_name": True}
    assert len(results) == 3
    assert results[0]["code"] == tags.product2["code"]
    assert results[1]["code"] == tags.product3["code"]
    assert results[2]["code"] == tags.product1["code"]


@patch.object(query, "find_products")
async def test_limit_and_offset(mocked_mongo):
    tags = await create_tags_and_scans()

    # Using world so order should be 2,3,1 but skipping 2 and limiting to 1
    patch_context_manager(
        mocked_mongo,
        mock_cursor(
            [
                {"code": tags.product3["code"]},
            ]
        ),
    )
    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True, "product_name": True},
            sort=[("popularity_key", -1)],
            skip=1,
            limit=1,
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 1
    assert call_args[0][1] == {"code": True, "product_name": True}
    assert len(results) == 1
    assert results[0]["code"] == tags.product3["code"]


@patch.object(query, "find_products")
async def test_obsolete(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(
        mocked_mongo,
        mock_cursor(
            [
                {"code": tags.product4["code"]},
            ]
        ),
    )
    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True, "product_name": True},
            sort=[("popularity_key", -1)],
        ),
        True,
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert len(call_args[0][0]["_id"]["$in"]) == 1
    assert call_args[0][2] == True
    assert len(results) == 1
    assert results[0]["code"] == tags.product4["code"]


@patch.object(query, "get_loaded_tags", return_value=[])
async def test_exception_when_scans_not_loaded(_):
    with pytest.raises(HTTPException) as e:
        await query.find(
            FindQuery(
                filter=Filter(),
                projection={"code": True},
                sort=[("popularity_key", -1)],
                limit=50,
            ),
            True,
        )
    assert e.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_exception_when_sort_key_not_supported():
    with pytest.raises(ValidationError) as e:
        await query.find(
            FindQuery(
                filter=Filter(),
                projection={"code": True},
                sort=[("code", -1)],
                limit=50,
            ),
            True,
        )
    main_error = e.value.errors()[0]
    assert main_error["loc"][0] == "sort"


async def test_returns_data_when_no_sort_specified():
    tags = await create_tags_and_scans()

    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True},
        )
    )
    assert len(results) == 3


async def test_returns_data_when_ascending_sort_specified():
    tags = await create_tags_and_scans()

    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True},
            sort=[(SortColumn.product_name, 1)],
        )
    )
    assert len(results) == 3
    assert results[0]["code"] == tags.product2["code"]
    assert results[1]["code"] == tags.product3["code"]
    assert results[2]["code"] == tags.product1["code"]


async def test_sort_by_total_scans():
    tags = await create_tags_and_scans()

    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True},
            sort=[(SortColumn.unique_scans_n, -1)],
        )
    )
    assert len(results) == 3
    assert results[0]["code"] == tags.product2["code"]
    assert results[1]["code"] == tags.product3["code"]
    assert results[2]["code"] == tags.product1["code"]


@patch.object(query, "find_products")
async def test_mongo_not_called_if_just_requesting_codes(mocked_mongo):
    tags = await create_tags_and_scans()

    results = await query.find(
        FindQuery(
            filter=Filter(origins_tags=tags.origin_value),
            projection={"code": True},
            sort=[("popularity_key", -1)],
        )
    )
    assert not mocked_mongo.called
    assert len(results) == 3
    assert results[0]["code"] == tags.product2["code"]
    assert results[1]["code"] == tags.product3["code"]
    assert results[2]["code"] == tags.product1["code"]


@patch.object(query, "find_products")
async def test_null_projection_passed_through_to_mongodb(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(
        mocked_mongo,
        mock_cursor(
            [
                {"code": tags.product1["code"]},
            ]
        ),
    )
    results = await query.find(
        FindQuery(
            filter=Filter(countries_tags=tags.country["tag"]),
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert call_args[0][1] == None
    assert results[0]["code"] == tags.product1["code"]


@patch.object(query, "find_products")
async def test_empty_projection_passed_through_to_mongodb(mocked_mongo):
    tags = await create_tags_and_scans()

    patch_context_manager(
        mocked_mongo,
        mock_cursor(
            [
                {"code": tags.product1["code"]},
            ]
        ),
    )
    results = await query.find(
        FindQuery(
            filter=Filter(countries_tags=tags.country["tag"]),
            projection={},
        )
    )
    assert mocked_mongo.called
    call_args = mocked_mongo.call_args
    assert call_args[0][1] == {}
    assert results[0]["code"] == tags.product1["code"]


async def test_gt_lt_operators():
    tags = await create_tags_and_scans()

    results = await query.find(
        FindQuery(
            filter=Filter(
                qualify_and=[
                    Fragment(origins_tags=tags.origin_value),
                    Fragment(additives_n=Qualify(qualify_gt=1)),
                    Fragment(additives_n=Qualify(qualify_lt=3)),
                ],
            ),
            projection={"code": True},
        )
    )
    assert len(results) == 1
    assert results[0]["code"] == tags.product2["code"]


async def test_gte_lte_operators():
    tags = await create_tags_and_scans()

    results = await query.find(
        FindQuery(
            filter=Filter(
                qualify_and=[
                    Fragment(origins_tags=tags.origin_value),
                    Fragment(additives_n=Qualify(qualify_gte=2)),
                    Fragment(additives_n=Qualify(qualify_lte=3)),
                ],
            ),
            projection={"code": True},
            sort=[(SortColumn.product_name, 1)],
        )
    )
    assert len(results) == 2
    assert results[0]["code"] == tags.product2["code"]
    assert results[1]["code"] == tags.product3["code"]


async def test_nutrient_filter():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    results = await query.find(
        FindQuery(
            filter=Filter(
                **{f"{NUTRIENT_TAG}.{tags.nutrient_tag}_100g": Qualify(qualify_lt=0.2)}
            ),
            projection={"code": True},
        )
    )
    assert len(results) == 1
    assert results[0]["code"] == tags.product1["code"]


async def test_new_nutrition_filter():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    results = await query.find(
        FindQuery(
            filter=Filter(
                **{f"{NUTRITION_TAG}.{tags.nutrient_tag}": Qualify(qualify_lt=0.2)}
            ),
            projection={"code": True},
        )
    )
    assert len(results) == 1
    assert results[0]["code"] == tags.product1["code"]


async def create_tags_and_scans():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)
        world = await get_country(transaction, "en:world")
        # Country sequence should be: 3,2,1. World sequence: 2,3,1
        await create_scan(transaction, tags.product1, tags.country, TEST_YEAR, 10)
        await create_scan(transaction, tags.product1, world, TEST_YEAR, 20)
        await create_product_scan(transaction, tags.product1, TEST_YEAR, 30, 30)

        await create_scan(transaction, tags.product2, tags.country, TEST_YEAR, 100)
        await create_scan(transaction, tags.product2, world, TEST_YEAR, 201)
        await create_product_scan(transaction, tags.product2, TEST_YEAR, 301, 301)

        await create_scan(transaction, tags.product3, world, TEST_YEAR - 1, 100)
        await create_scan(transaction, tags.product3, tags.country, TEST_YEAR - 1, 1)
        await create_product_scan(transaction, tags.product3, TEST_YEAR - 1, 101, 101)
        await create_scan(transaction, tags.product3, world, TEST_YEAR, 200)
        await create_scan(transaction, tags.product3, tags.country, TEST_YEAR, 100)
        await create_product_scan(transaction, tags.product3, TEST_YEAR, 300, 300)

        await create_scan(transaction, tags.product4, world, TEST_YEAR, 50)
        await create_scan(transaction, tags.product4, tags.country, TEST_YEAR, 50)
        await create_product_scan(transaction, tags.product4, TEST_YEAR, 100, 100)

        # Make sure scans are flagged as fully loaded
        with patch.object(scan, "get_current_scan_year", return_value=TEST_YEAR) as _:
            await scans_fully_loaded(transaction)

        return tags
