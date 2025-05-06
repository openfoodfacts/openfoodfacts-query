"""Global test configuration and setup / teardown functions"""

import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from .config import config_settings
from .migrator import migrate_database


# Don't prefix with "Test" as otherwise pytest thinks this is a test class
class SettingsForTests(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".envrc"), extra="ignore")

    POSTGRES_IMAGE: str
    USE_TESTCONTAINERS: bool


test_settings = SettingsForTests()


@pytest.fixture(scope="session", autouse=True)
async def setup(request):
    """You can use your local PostgreSQL database and Redis instances for tests by disabling test containers
    This runs a bit faster but doesn't test migrations"""
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

    # Always run migrations, even if not using testcontainers
    await migrate_database(True)
