import query.repositories.products as products
import query.repositories.product_tags as product_tags
import query.repositories.product_ingredients as product_ingredients

async def up(connection):
    # Changing product id from a UUID to an integer. Migration steps are as follows:
    # 1. Drop all existing primary keys that reference product_id (CASCADE removes foreign keys too)
    # 2. Drop old value index
    # 3. Rename old product id column
    # 4. Add new integer product id column
    # 5. Update new column for tags
    # 6. Make column not null
    # 7. Add back primary keys
    # 8. Add product id index
    # 9. Add back foreign keys
    # 10. Drop old column

    # 1. Drop all existing primary keys that reference product_id (CASCADE removes foreign keys too)
    await product_tags.drop_old_id(connection)
    await product_ingredients.drop_old_id(connection)

    await products.change_primary_key(connection)

    # 2. Drop old value index
    # 3. Rename old product id column

    # 5. Update new column for tags
    await product_tags.populate_new_product_id(connection)
    await product_ingredients.populate_new_product_id(connection)
    await products.drop_old_id(connection)

