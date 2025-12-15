from query.tables.product_update_event import add_message_id_constraint


async def up(transaction):
    await add_message_id_constraint(transaction)
