from asyncpg import Connection


async def create_table(transaction: Connection):
    await transaction.execute(
        """CREATE TEMP TABLE IF NOT EXISTS product_temp (id int PRIMARY KEY, last_updated timestamptz, data jsonb) ON COMMIT DELETE ROWS"""
    )
