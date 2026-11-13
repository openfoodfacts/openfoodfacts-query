from query.tables import settings


async def up(transaction):
    await settings.add_bulk_message_id(transaction)
