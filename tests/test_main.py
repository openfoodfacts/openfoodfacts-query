from fastapi.testclient import TestClient
from query.db import Database
from query.main import app
from tests.test_query import create_test_tags


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
