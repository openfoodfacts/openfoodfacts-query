from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from typing import Any, Dict

from query.models.query import Filter
from query.config import config_settings


@asynccontextmanager
async def find_products(filter: Dict[str, Any], projection: Dict[str,bool], obsolete = False):
    client = AsyncIOMotorClient(config_settings.MONGO_URI, serverSelectionTimeoutMS=1000)
    db = client.get_database('off')
    collection = db.get_collection('products')
    cursor = collection.find(filter, projection)
    try:
        yield cursor
    finally:
        await cursor.close()
        #await client.close()
