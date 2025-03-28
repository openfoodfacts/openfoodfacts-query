from query.tables import product_country


async def up(connection):
    await product_country.fix_index(connection)
