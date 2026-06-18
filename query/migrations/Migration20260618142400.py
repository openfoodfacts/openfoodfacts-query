from query.tables import product_update


async def up(transaction):
    # Delete products where the code doesn't match current conventions
    await transaction.execute(
        """DELETE FROM product WHERE (length(code) > 13 and code LIKE '0%')
                              OR (length(code) < 13 and length(code) <> 8);"""
    )
    await product_update.migration_add_product_foreign_key(transaction)
