"""Routines for interacting with MongoDB"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from pymongo import AsyncMongoClient

from query.tables.collection_type import (
    BEAUTY,
    BEAUTY_OBSOLETE,
    FOOD,
    FOOD_OBSOLETE,
    PETFOOD,
    PETFOOD_OBSOLETE,
    PRODUCT,
    PRODUCT_OBSOLETE,
)

from .config import config_settings

# Limit the MongoDB logging as it is a bit verbose
logging.getLogger("pymongo").setLevel(logging.WARNING)
mongo_dbs = {
    FOOD: ["off", "products"],
    FOOD_OBSOLETE: ["off", "products_obsolete"],
    PETFOOD: ["opff", "products"],
    PETFOOD_OBSOLETE: ["opff", "products_obsolete"],
    BEAUTY: ["obf", "products"],
    BEAUTY_OBSOLETE: ["obf", "products_obsolete"],
    PRODUCT: ["opf", "products"],
    PRODUCT_OBSOLETE: ["opf", "products_obsolete"],
}


@asynccontextmanager
async def find_products(
    filter: Dict[str, Any], projection: Dict[str, bool], collection=FOOD
):
    """Runs a query on the MongoDB products collection with the specified filter and projection and returns a cursor"""
    client = AsyncMongoClient(config_settings.MONGO_URI, serverSelectionTimeoutMS=2000)
    mongo_db = mongo_dbs[collection]
    db = client.get_database(mongo_db[0])
    collection = db.get_collection(mongo_db[1])
    cursor = collection.find(filter, projection)
    try:
        yield cursor
    finally:
        await cursor.close()
