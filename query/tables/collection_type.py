"""The collection groups products by their product type and whether they are deleted or obsolete
Stored in a combined table to minimise the number of columns we have to index by.
Note this is not referenced as a foreign key by other tables to minimise update time
so this table is really just reference for the enumeration"""

async def create_table(transaction):
    await transaction.execute("""CREATE TABLE IF NOT EXISTS collection (
      id smallint NOT NULL,
      product_type text NOT NULL,
      obsolete boolean NOT NULL,
      deleted boolean NOT NULL,
      constraint collection_pkey primary key (id))""")

    # Add standard values
    await transaction.execute("""INSERT INTO collection (id, product_type, obsolete, deleted) VALUES
        (10, 'food', FALSE, FALSE),
        (11, 'food', TRUE, FALSE),
        (12, 'food', FALSE, TRUE),
        (20, 'petfood', FALSE, FALSE),
        (21, 'petfood', TRUE, FALSE),
        (22, 'petfood', FALSE, TRUE),
        (30, 'beauty', FALSE, FALSE),
        (31, 'beauty', TRUE, FALSE),
        (32, 'beauty', FALSE, TRUE),
        (40, 'product', FALSE, FALSE),
        (41, 'product', TRUE, FALSE),
        (42, 'product', FALSE, TRUE)""")

