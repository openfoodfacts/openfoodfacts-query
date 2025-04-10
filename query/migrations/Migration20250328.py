from query.tables import product_country


async def up(transaction):
    await product_country.fix_index(transaction)
