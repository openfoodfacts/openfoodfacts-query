from query.tables.product_scans import create_product_scans_table


async def up(transaction):
    await create_product_scans_table(transaction)
