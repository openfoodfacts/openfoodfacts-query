from unittest.mock import patch

import pytest
from fastapi import HTTPException, status
from pydantic import ValidationError

from ..database import get_transaction
from ..models.query import Filter, FindQuery
from ..services import query
from ..services.query_count_test import create_test_tags
from ..tables.country import get_country
from ..tables.product_country import CURRENT_YEAR, PRODUCT_COUNTRY_TAG
from ..tables.product_scans_by_country import create_scan
from ..test_helper import mock_cursor, patch_context_manager
from . import query


@patch.object(query, "get_loaded_tags", return_value=[PRODUCT_COUNTRY_TAG])
@patch.object(query, "find_products")
async def test_sorts_by_country_scans(mocked_mongo, _):
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


@patch.object(
    query,
    "get_loaded_tags",
    return_value=[PRODUCT_COUNTRY_TAG, "origins_tags"],
)
@patch.object(query, "find_products")
async def test_sorts_by_world_scans(mocked_mongo, _):
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


@patch.object(
    query,
    "get_loaded_tags",
    return_value=[PRODUCT_COUNTRY_TAG, "origins_tags"],
)
@patch.object(query, "find_products")
async def test_limit_and_offset(mocked_mongo, _):
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


@patch.object(
    query,
    "get_loaded_tags",
    return_value=[PRODUCT_COUNTRY_TAG, "origins_tags"],
)
@patch.object(query, "find_products")
async def test_obsolete(mocked_mongo, _):
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
    assert e.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_exception_when_sort_not_popularity_key():
    with pytest.raises(ValidationError) as e:
        await query.find(
            FindQuery(
                filter=Filter(),
                projection={"code": True},
                sort=[("last_modified_t", -1)],
                limit=50,
            ),
            True,
        )
    main_error = e.value.errors()[0]
    assert main_error["loc"][0] == "sort"


async def test_exception_when_no_sort_specified():
    with pytest.raises(HTTPException) as e:
        await query.find(
            FindQuery(filter=Filter(), projection={"code": True}, sort=[], limit=50),
            True,
        )
    assert e.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_exception_when_ascending_sort_specified():
    with pytest.raises(HTTPException) as e:
        await query.find(
            FindQuery(
                filter=Filter(),
                projection={"code": True},
                sort=[("popularity_key", 1)],
                limit=50,
            ),
            True,
        )
    assert e.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@patch.object(
    query,
    "get_loaded_tags",
    return_value=[PRODUCT_COUNTRY_TAG, "origins_tags"],
)
@patch.object(query, "find_products")
async def test_mongo_not_called_if_just_requesting_codes(mocked_mongo, _):
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


async def create_tags_and_scans():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)
        world = await get_country(transaction, "en:world")
        # Country sequence should be: 3,2,1. World sequence: 2,3,1
        await create_scan(transaction, tags.product1, tags.country, CURRENT_YEAR, 10)
        await create_scan(transaction, tags.product2, tags.country, CURRENT_YEAR, 100)
        await create_scan(transaction, tags.product3, tags.country, CURRENT_YEAR, 100)
        await create_scan(transaction, tags.product3, tags.country, CURRENT_YEAR - 1, 1)
        await create_scan(transaction, tags.product4, tags.country, CURRENT_YEAR, 50)
        await create_scan(transaction, tags.product1, world, CURRENT_YEAR, 20)
        await create_scan(transaction, tags.product2, world, CURRENT_YEAR, 201)
        await create_scan(transaction, tags.product3, world, CURRENT_YEAR, 200)
        await create_scan(transaction, tags.product3, world, CURRENT_YEAR - 1, 100)
        await create_scan(transaction, tags.product4, world, CURRENT_YEAR, 50)

        return tags
