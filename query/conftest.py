from pydantic_settings import BaseSettings, SettingsConfigDict
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
import pytest
from query.database import database_connection, config_settings
from query.migrator import migrate_database


# Don't prefix with "Test" as otherwise pytest thinks this is a test class
class SettingsForTests(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_IMAGE: str


test_settings = SettingsForTests()

# Comment out below code to use existing database for testing (faster)

# postgres = PostgresContainer(test_settings.POSTGRES_IMAGE)
# redis = RedisContainer()

# @pytest.fixture(scope="session", autouse=True)
# async def setup(request):
#     postgres.start()
#     redis.start()

#     def remove_container():
#         postgres.stop()
#         redis.stop()

#     request.addfinalizer(remove_container)
#     config_settings.POSTGRES_HOST = (
#         f"{postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}"
#     )
#     config_settings.POSTGRES_DB = postgres.dbname
#     config_settings.POSTGRES_USER = postgres.username
#     config_settings.POSTGRES_PASSWORD = postgres.password

#     config_settings.REDIS_URL = (
#         f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}"
#     )

#     async with Database() as conn:
#         await migrate_database(conn)
