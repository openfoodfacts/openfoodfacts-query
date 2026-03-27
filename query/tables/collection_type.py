"""The collection groups products by their product type and whether they are deleted or obsolete
Stored in a combined table to minimise the number of columns we have to index by.
Note this is not referenced as a foreign key by other tables to minimise update time
so this table is really just reference for the enumeration"""

FOOD = 10
FOOD_OBSOLETE = 11
FOOD_DELETED = 12
PETFOOD = 20
PETFOOD_OBSOLETE = 21
PETFOOD_DELETED = 22
BEAUTY = 30
BEAUTY_OBSOLETE = 31
BEAUTY_DELETED = 32
PRODUCT = 40
PRODUCT_OBSOLETE = 41
PRODUCT_DELETED = 42


async def create_table(transaction):
    await transaction.execute("""CREATE TABLE IF NOT EXISTS collection (
      id smallint NOT NULL,
      product_type text NOT NULL,
      obsolete boolean NOT NULL,
      deleted boolean NOT NULL,
      constraint collection_pkey primary key (id))""")

    # Add standard values
    await transaction.execute(
        f"""INSERT INTO collection (id, product_type, obsolete, deleted) VALUES
        ({FOOD}, 'food', FALSE, FALSE),
        ({FOOD_OBSOLETE}, 'food', TRUE, FALSE),
        ({FOOD_DELETED}, 'food', FALSE, TRUE),
        ({PETFOOD}, 'petfood', FALSE, FALSE),
        ({PETFOOD_OBSOLETE}, 'petfood', TRUE, FALSE),
        ({PETFOOD_DELETED}, 'petfood', FALSE, TRUE),
        ({BEAUTY}, 'beauty', FALSE, FALSE),
        ({BEAUTY_OBSOLETE}, 'beauty', TRUE, FALSE),
        ({BEAUTY_DELETED}, 'beauty', FALSE, TRUE),
        ({PRODUCT}, 'product', FALSE, FALSE),
        ({PRODUCT_OBSOLETE}, 'product', TRUE, FALSE),
        ({PRODUCT_DELETED}, 'product', FALSE, TRUE)"""
    )
