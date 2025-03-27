from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import asyncpg
from query.config import config_settings
from query.database import database_connection
from query.services.event_test import sample_event
from query.tables.product_update_event import create_events
from query.test_helper import random_code


@asynccontextmanager
async def readonly_connection() -> AsyncGenerator[asyncpg.Connection, Any]:
    connection = await asyncpg.connect(
        user=config_settings.VIEW_USER,
        password=config_settings.VIEW_PASSWORD,
        database=config_settings.POSTGRES_DB,
        host=config_settings.POSTGRES_HOST.split(":")[0],
        port=config_settings.POSTGRES_HOST.split(":")[-1],
    )
    try:
        yield connection
    finally:
        await connection.close()


async def test_aggregate_events_by_count_and_distinct_products():
    async with database_connection() as connection:
        # create some products
        code1 = random_code()
        code2 = random_code()
        owner1 = random_code()
        await connection.execute(
            "insert into product (code, owners_tags) values ($1, $3), ($2, $3)",
            code1,
            code2,
            owner1,
        )

        # create some messages
        await create_events(
            connection,
            [
                sample_event(
                    {"code": code1, "user_id": "user1", "action": "updated", "rev": 1}
                ),
                sample_event(
                    {"code": code1, "user_id": "user1", "action": "updated", "rev": 2}
                ),
                sample_event(
                    {"code": code1, "user_id": "user1", "action": "updated", "rev": 3}
                ),
                sample_event(
                    {"code": code2, "user_id": "user1", "action": "updated", "rev": 1}
                ),
            ],
        )

    # use viewer user
    async with readonly_connection() as viewer:
        results = await viewer.fetch(
            "select * from product_updates_by_owner where owner_tag = $1", owner1
        )
        assert len(results) == 1
        assert results[0]["update_count"] == 4
        assert results[0]["product_count"] == 2


async def test_update_existing_aggregate_counts():
    async with database_connection() as connection:
        # create a product
        code1 = random_code()
        await connection.execute("insert into product (code) values ($1)", code1)

        # create an existing message
        action1 = random_code()
        await create_events(
            connection,
            [
                sample_event(
                    {"code": code1, "user_id": "user1", "action": action1, "rev": 1}
                ),
            ],
        )

        # add another message
        await create_events(
            connection,
            [
                sample_event(
                    {"code": code1, "user_id": "user1", "action": action1, "rev": 2}
                ),
            ],
        )

    # use viewer user
    async with readonly_connection() as viewer:
        results = await viewer.fetch(
            "select * from product_updates_by_owner where update_type = $1", action1
        )
        assert len(results) == 1
        assert results[0]["update_count"] == 2
        assert results[0]["product_count"] == 1
