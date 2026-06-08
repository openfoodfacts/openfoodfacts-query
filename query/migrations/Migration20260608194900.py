from query.tables import product_country


async def up(transaction):
    await product_country.migration_fix_index(transaction)