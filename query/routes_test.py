from contextlib import asynccontextmanager

from fastapi import status
from httpx import ASGITransport, AsyncClient

from query.database import get_transaction
from query.routes import app
from query.services.query_count_test import create_test_tags
from query.services.query_find_test import create_tags_and_scans


@asynccontextmanager
async def get_test_client():
    """A reusable helper function that yields a safe async client context."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


async def test_count_route():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    async with get_test_client() as client:
        response = await client.post(
            "/count",
            json={
                "amino_acids_tags": {"$ne": tags.amino_value},
                "origins_tags": tags.origin_value,
            },
        )
        assert response.status_code == 200
        assert response.json() == 1


async def test_count_route_with_product_type():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    async with get_test_client() as client:
        response = await client.post(
            "/count?product_type=petfood",
            json={"origins_tags": tags.origin_value},
        )
        assert response.status_code == 200
        assert response.json() == 0


async def test_count_obsolete():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    async with get_test_client() as client:

        response = await client.post(
            "/count?obsolete=1", json={"origins_tags": tags.origin_value}
        )
        assert response.status_code == 200
        assert response.json() == 1


async def test_count_invalid_tag():
    async with get_test_client() as client:

        response = await client.post("/count", json={"invalid_tag": "z"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert "invalid_tag" in response.text


async def test_count_invalid_qualifier():
    async with get_test_client() as client:

        response = await client.post(
            "/count", json={"origins_tags": {"$invalid": [1, 2]}}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert "$invalid" in response.text


async def test_aggregate_obsolete():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    async with get_test_client() as client:
        response = await client.post(
            "/aggregate?obsolete=1",
            json=[
                {"$match": {"amino_acids_tags": tags.amino_value}},
                {"$group": {"_id": "$origins_tags"}},
            ],
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]["_id"] == tags.origin_value
        assert response_data[0]["count"] == 1


async def test_find_just_code():
    tags = await create_tags_and_scans()
    async with get_test_client() as client:
        response = await client.post(
            "/find",
            json={
                "filter": {"origins_tags": tags.origin_value},
                "projection": {"code": 1},
                "sort": [["popularity_key", -1]],
            },
        )
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert len(results) == 3
        assert results[0]["code"] == tags.product2["code"]
        assert results[1]["code"] == tags.product3["code"]
        assert results[2]["code"] == tags.product1["code"]
