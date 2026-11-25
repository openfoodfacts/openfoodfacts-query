"""Various helper functions used during tests"""

import asyncio
from unittest.mock import Mock
from uuid import uuid4

from query.database import get_transaction


def random_code():
    return str(uuid4())


async def mock_cursor(data):
    for item in data:
        yield item


async def error_cursor(message):
    for index in range(1):
        # Need to include a yield so that an async iterator is created
        if False:
            yield index
        raise Exception(message)


def patch_context_manager(mock: Mock, *cursors):
    """Patching a context manager isn't very intuitive so use this simple helper function to do it"""
    # Clone the list so we don't modify what is passed in
    cursor_list = list(cursors)

    def next_cursor():
        nonlocal cursor_list
        return cursor_list.pop(0) if cursor_list else mock_cursor([])

    mock.return_value.__aenter__.side_effect = next_cursor


async def wait_for_postgres_sleep(pid: int):
    """Wait until PostgreSQL is executing pg_sleep for the given connection."""
    async with get_transaction() as observer:
        async with asyncio.timeout(5):
            while True:
                # PostgreSQL reports an executing pg_sleep as active, with
                # PgSleep as its wait event. An idle connection cannot match.
                is_sleeping = await observer.fetchval(
                    """
                    SELECT state = 'active' AND wait_event = 'PgSleep'
                    FROM pg_stat_activity WHERE pid = $1
                    """,
                    pid,
                )
                if is_sleeping:
                    return
                await asyncio.sleep(0.01)
