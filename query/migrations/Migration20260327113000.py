from query.tables import (
    collection_type,
    product,
    product_country,
    product_ingredient,
    product_tags,
)


async def up(transaction):
    await collection_type.create_table(transaction)
    await product.migration_add_collection(transaction)
    await product_tags.migration_add_collection(transaction)
    await product_ingredient.migration_add_collection(transaction)
    await product_country.migration_add_collection(transaction)
