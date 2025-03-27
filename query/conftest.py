from pydantic_settings import BaseSettings, SettingsConfigDict
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
import pytest
from query.database import database_connection
from query.migrator import migrate_database
from query.config import config_settings
from query.redis import STREAM_NAME, redis_client
from query.redis_test import add_test_message
from query.test_helper import random_code


# Don't prefix with "Test" as otherwise pytest thinks this is a test class
class SettingsForTests(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".envrc"), extra="ignore")

    POSTGRES_IMAGE: str
    USE_TESTCONTAINERS: bool


test_settings = SettingsForTests()


@pytest.fixture(scope="session", autouse=True)
async def setup(request):
    if test_settings.USE_TESTCONTAINERS:
        postgres = PostgresContainer(test_settings.POSTGRES_IMAGE)
        redis = RedisContainer()

        postgres.start()
        redis.start()

        def remove_container():
            postgres.stop()
            redis.stop()

        request.addfinalizer(remove_container)
        config_settings.POSTGRES_HOST = (
            f"{postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}"
        )
        config_settings.POSTGRES_DB = postgres.dbname
        config_settings.POSTGRES_USER = postgres.username
        config_settings.POSTGRES_PASSWORD = postgres.password

        config_settings.REDIS_URL = (
            f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}"
        )

        async with database_connection() as conn:
            await migrate_database(conn)
