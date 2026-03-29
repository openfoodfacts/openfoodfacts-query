"""The collection groups products by their product type and whether they are deleted or obsolete
Stored in a combined table to minimise the number of columns we have to index by.
Note this is not referenced as a foreign key by other tables to minimise update time
so this table is really just reference for the enumeration"""

from datetime import datetime
from enum import Enum

DELETED = 1
FOOD = 10
FOOD_OBSOLETE = 11
PETFOOD = 20
PETFOOD_OBSOLETE = 21
BEAUTY = 30
BEAUTY_OBSOLETE = 31
PRODUCT = 40
PRODUCT_OBSOLETE = 41


class ProductType(str, Enum):
    """The product type to search for"""

    food = "food"
    petfood = "petfood"
    beauty = "beauty"
    product = "product"

SUPPORTED_PRODUCT_TYPES = [item.value for item in ProductType]

COLLECTION_MAP = {
    ProductType.food: {False: FOOD, True: FOOD_OBSOLETE},
    ProductType.petfood: {False: PETFOOD, True: PETFOOD_OBSOLETE},
    ProductType.beauty: {False: BEAUTY, True: BEAUTY_OBSOLETE},
    ProductType.product: {False: PRODUCT, True: PRODUCT_OBSOLETE},
}


async def create_table(transaction):
    await transaction.execute("""CREATE TABLE IF NOT EXISTS collection (
      id smallint NOT NULL,
      product_type text NOT NULL,
      obsolete boolean NOT NULL,
      deleted boolean NOT NULL,
      last_updated timestamptz NULL,
      constraint collection_pkey primary key (id))""")

    # Add standard values
    await transaction.execute(
        f"""INSERT INTO collection (id, product_type, obsolete, deleted) VALUES
        ({DELETED}, 'deleted', FALSE, TRUE),
        ({FOOD}, '{ProductType.food}', FALSE, FALSE),
        ({FOOD_OBSOLETE}, '{ProductType.food}', TRUE, FALSE),
        ({PETFOOD}, '{ProductType.petfood}', FALSE, FALSE),
        ({PETFOOD_OBSOLETE}, '{ProductType.petfood}', TRUE, FALSE),
        ({BEAUTY}, '{ProductType.beauty}', FALSE, FALSE),
        ({BEAUTY_OBSOLETE}, '{ProductType.beauty}', TRUE, FALSE),
        ({PRODUCT}, '{ProductType.product}', FALSE, FALSE),
        ({PRODUCT_OBSOLETE}, '{ProductType.product}', TRUE, FALSE)"""
    )
    await transaction.execute(
        f"""UPDATE collection SET last_updated = (SELECT last_updated FROM settings) WHERE id IN ({FOOD},{FOOD_OBSOLETE})"""
    )


async def get_last_updated(transaction, collection_id) -> datetime:
    """The most recent last_updated date for a product in the PostgreSQL database"""
    return await transaction.fetchval(
        "SELECT last_updated FROM collection WHERE id = $1", collection_id
    )


async def set_last_updated(transaction, collection_id, last_updated):
    await transaction.execute(
        "UPDATE collection SET last_updated = $2 WHERE id = $1",
        collection_id,
        last_updated,
    )
