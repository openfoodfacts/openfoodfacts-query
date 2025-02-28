import os
from pydantic_settings import BaseSettings, SettingsConfigDict
import pytest
from unittest.mock import Mock, patch
from query.main import HealthStatusEnum, health
from query.db import Database, settings
from testcontainers.postgres import PostgresContainer

from query.migrator import migrate_database


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_IMAGE: str


test_settings = TestSettings()

postgres = PostgresContainer(test_settings.POSTGRES_IMAGE)


@pytest.fixture(scope="module", autouse=True)
async def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    settings.POSTGRES_HOST = (
        f"{postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}"
    )
    settings.POSTGRES_DB = postgres.dbname
    settings.POSTGRES_USER = postgres.username
    settings.POSTGRES_PASSWORD = postgres.password

    async with Database() as conn:
        await migrate_database(conn)


class MockMongoClient:
    class Admin:
        async def command(*args):
            pass

    admin = Admin()


@patch("query.main.AsyncIOMotorClient", return_value=MockMongoClient())
async def test_health_ok(mocked_mongo):
    my_health = await health()
    assert mocked_mongo.called
    assert my_health.status == HealthStatusEnum.ok


@patch("query.main.AsyncIOMotorClient", side_effect=Exception("mongodb is down"))
async def test_health_should_return_unhealthy_if_mongodb_is_down(mocked_mongo):
    my_health = await health()
    assert mocked_mongo.called
    assert my_health.status == HealthStatusEnum.error
