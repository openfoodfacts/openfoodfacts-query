import asyncio

from query.database import get_transaction
from query.tables.settings import set_pre_migration_message_id


async def test_migration_doesnt_start_until_imports_are_finished():
    """Test that if an import is running then a migration doesn't start until it finishes"""
    async with get_transaction() as transaction:
        # Lock the settings table as if we were doing an import
        await transaction.fetchval(
            "SELECT pre_migration_message_id FROM settings FOR UPDATE"
        )
        task = asyncio.create_task(set_pre_migration_message_id())
        await asyncio.sleep(0.1)

        assert not task.done()
    await task
    assert task.done()
