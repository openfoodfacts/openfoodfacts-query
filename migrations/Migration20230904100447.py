import query.repositories.products as products
import query.repositories.product_tags as product_tags
import query.repositories.loaded_tags as loaded_tags
import query.repositories.product_ingredients as product_ingredients
import query.repositories.settings as settings

async def up(connection):
    await products.create_table(connection)
    await product_tags.create_tables(connection)
    await loaded_tags.create_table(connection)
    await product_ingredients.create_table(connection)
    await settings.create_table(connection)