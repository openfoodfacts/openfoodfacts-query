from fastapi import status
from fastapi.testclient import TestClient

from query.services.query_find_test import create_tags_and_scans

from .database import get_transaction
from .routes import app
from .services.query_count_test import create_test_tags


async def test_count_route():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    client = TestClient(app)

    response = client.post(
        "/count",
        json={
            "amino_acids_tags": {"$ne": tags.amino_value},
            "origins_tags": tags.origin_value,
        },
    )
    assert response.status_code == 200
    assert response.json() == 1


async def test_count_obsolete():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    client = TestClient(app)

    response = client.post(
        "/count?obsolete=1", json={"origins_tags": tags.origin_value}
    )
    assert response.status_code == 200
    assert response.json() == 1


async def test_count_invalid_tag():
    client = TestClient(app)

    response = client.post("/count", json={"invalid_tag": "z"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "invalid_tag" in response.text


async def test_count_invalid_qualifier():
    client = TestClient(app)

    response = client.post("/count", json={"origins_tags": {"$invalid": [1, 2]}})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "$invalid" in response.text


async def test_aggregate_obsolete():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)
    client = TestClient(app)
    response = client.post(
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
    client = TestClient(app)
    response = client.post(
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
