from query.tables import (
    collection_type,
)


async def up(transaction):
    await collection_type.migration_add_last_updated(transaction)
