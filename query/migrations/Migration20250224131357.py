from ..tables import country, product_country, product_scans_by_country


async def up(transaction):
    await country.create_table(transaction)
    await product_scans_by_country.create_table(transaction)
    await product_country.create_table(transaction)
