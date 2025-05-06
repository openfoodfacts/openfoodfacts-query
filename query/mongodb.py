"""Routines for interacting with MongoDB"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorClient

from .config import config_settings

# Limit the MongoDB logging as it is a bit verbose
logging.getLogger("pymongo").setLevel(logging.WARNING)


@asynccontextmanager
async def find_products(
    filter: Dict[str, Any], projection: Dict[str, bool], obsolete=False
):
    """Runs a query on the MongoDB products collection with the specified filter and projection and returns a cursor"""
    client = AsyncIOMotorClient(
        config_settings.MONGO_URI, serverSelectionTimeoutMS=1000
    )
    db = client.get_database("off")
    collection = db.get_collection(f"products{'_obsolete' if obsolete else ''}")
    cursor = collection.find(filter, projection)
    try:
        yield cursor
    finally:
        await cursor.close()
