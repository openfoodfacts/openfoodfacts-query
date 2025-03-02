import query.repositories.product as product
import query.repositories.product_tags as product_tags
import query.repositories.loaded_tag as loaded_tag
import query.repositories.product_ingredient as product_ingredient
import query.repositories.settings as settings

async def up(connection):
    await product.create_table(connection)
    await product_tags.create_tables(connection)
    await loaded_tag.create_table(connection)
    await product_ingredient.create_table(connection)
    await settings.create_table(connection)