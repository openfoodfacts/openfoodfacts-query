from ..tables import product_country


async def up(transaction):
    await product_country.delete_product_countries_with_no_tag(transaction)
