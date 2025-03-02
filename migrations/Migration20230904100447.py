import query.repositories.product as product
import query.repositories.product_tags as product_tags

async def up(connection):
    await product.create_table(connection)

    await product_tags.create_tables(connection)
