from query.tables import nutrient, product_nutrient, settings


async def up(transaction):
    await nutrient.create_table(transaction)
    await product_nutrient.create_table(transaction)
    await settings.add_pre_migration_message_id(transaction)
