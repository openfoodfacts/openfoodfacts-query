"""The collection groups products by their product type and whether they are deleted or obsolete
Stored in a combined table to minimise the number of columns we have to index by.
Note this is not referenced as a foreign key by other tables to minimise update time
so this table is really just reference for the enumeration"""

from query.models.query import ProductType


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
        ({FOOD}, '{ProductType.food}', FALSE, FALSE),
        ({FOOD_OBSOLETE}, '{ProductType.food}', TRUE, FALSE),
        ({FOOD_DELETED}, '{ProductType.food}', FALSE, TRUE),
        ({PETFOOD}, '{ProductType.petfood}', FALSE, FALSE),
        ({PETFOOD_OBSOLETE}, '{ProductType.petfood}', TRUE, FALSE),
        ({PETFOOD_DELETED}, '{ProductType.petfood}', FALSE, TRUE),
        ({BEAUTY}, '{ProductType.beauty}', FALSE, FALSE),
        ({BEAUTY_OBSOLETE}, '{ProductType.beauty}', TRUE, FALSE),
        ({BEAUTY_DELETED}, '{ProductType.beauty}', FALSE, TRUE),
        ({PRODUCT}, '{ProductType.product}', FALSE, FALSE),
        ({PRODUCT_OBSOLETE}, '{ProductType.product}', TRUE, FALSE),
        ({PRODUCT_DELETED}, '{ProductType.product}', FALSE, TRUE)"""
    )


COLLECTION_MAP = {
    ProductType.food: {False: FOOD, True: FOOD_OBSOLETE},
    ProductType.petfood: {False: PETFOOD, True: PETFOOD_OBSOLETE},
    ProductType.beauty: {False: BEAUTY, True: BEAUTY_OBSOLETE},
    ProductType.product: {False: PRODUCT, True: PRODUCT_OBSOLETE},
}
