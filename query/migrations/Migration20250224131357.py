from query.tables import country, product_country, product_scans_by_country


async def up(connection):
    await country.create_table(connection)
    await product_scans_by_country.create_table(connection)
    await product_country.create_table(connection)
