import os
from pydantic_settings import BaseSettings, SettingsConfigDict
import pytest
from unittest.mock import Mock, patch
from query.main import HealthStatusEnum, health, HealthItemStatusEnum
from query.db import Database, settings
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from query.migrator import migrate_database


# Don't prefix with "Test" as otherwise pytest thinks this is a test class
class SettingsForTests(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_IMAGE: str


test_settings = SettingsForTests()

postgres = PostgresContainer(test_settings.POSTGRES_IMAGE)
redis = RedisContainer()


@pytest.fixture(scope="module", autouse=True)
async def setup(request):
    postgres.start()
    redis.start()


    def remove_container():
        postgres.stop()
        redis.stop()

    request.addfinalizer(remove_container)
    settings.POSTGRES_HOST = (
        f"{postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}"
    )
    settings.POSTGRES_DB = postgres.dbname
    settings.POSTGRES_USER = postgres.username
    settings.POSTGRES_PASSWORD = postgres.password

    settings.REDIS_URL = f'redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}';

    async with Database() as conn:
        await migrate_database(conn)


class MockMongoClient:
    class Admin:
        async def command(*args):
            pass

    admin = Admin()


@patch("query.main.AsyncIOMotorClient", return_value=MockMongoClient())
async def test_health_should_return_healthy(mocked_mongo):
    my_health = await health()
    assert mocked_mongo.called
    assert my_health.status == HealthStatusEnum.ok
    assert my_health.info['postgres'].status == HealthItemStatusEnum.up
    assert my_health.info['mongodb'].status == HealthItemStatusEnum.up
    assert my_health.info['redis'].status == HealthItemStatusEnum.up


@patch("query.main.AsyncIOMotorClient", side_effect=Exception("mongodb is down"))
async def test_health_should_return_unhealthy_if_mongodb_is_down(mocked_mongo):
    my_health = await health()
    assert mocked_mongo.called
    assert my_health.status == HealthStatusEnum.error
    assert my_health.info['postgres'].status == HealthItemStatusEnum.up
    assert my_health.info['mongodb'].status == HealthItemStatusEnum.down
