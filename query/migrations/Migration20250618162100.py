from query.tables import nutrient, product_nutrient


async def up(transaction):
    await nutrient.create_table(transaction)
    await product_nutrient.create_table(transaction)