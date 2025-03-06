from fastapi.testclient import TestClient
from fastapi import status
from query.db import Database
from query.main import app
from query.services.query_count_test import create_test_tags


async def test_count_route():
    async with Database() as connection:
        tags = await create_test_tags(connection)
    
    client = TestClient(app)
    
    response = client.post("/count", json={"amino_acids_tags":{"$ne":tags.amino_value},"origins_tags":tags.origin_value})
    assert response.status_code == 200
    assert response.json() == 1


async def test_count_obsolete():
    async with Database() as connection:
        tags = await create_test_tags(connection)
    
    client = TestClient(app)
    
    response = client.post("/count?obsolete=1", json={"origins_tags":tags.origin_value})
    assert response.status_code == 200
    assert response.json() == 1


async def test_count_invalid_tag():
    client = TestClient(app)
    
    response = client.post("/count", json={"invalid_tag":"z"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "invalid_tag" in response.text


async def test_count_invalid_qualifier():
    client = TestClient(app)
    
    response = client.post("/count", json={"origins_tags":{"$invalid": [1,2]}})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "$invalid" in response.text
