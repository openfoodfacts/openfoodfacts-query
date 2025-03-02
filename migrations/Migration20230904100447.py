import query.tables.product as product
import query.tables.product_tags as product_tags
import query.tables.loaded_tag as loaded_tag
import query.tables.product_ingredient as product_ingredient
import query.tables.settings as settings

async def up(connection):
    await product.create_table(connection)
    await product_tags.create_tables(connection)
    await loaded_tag.create_table(connection)
    await product_ingredient.create_table(connection)
    await settings.create_table(connection)