from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from typing import Dict

from query.models.query import Filter
from query.config import config_settings


@asynccontextmanager
async def find_products(filter: Filter, projection: Dict[str,bool], obsolete = False):
    client = AsyncIOMotorClient(config_settings.MONGO_URI, serverSelectionTimeoutMS=1000)
    db = client.get_database('off')
    collection = db.get_collection('products')
    mongodbFilter = filter.model_dump(by_alias=True, exclude_defaults=True)
    cursor = collection.find(mongodbFilter, projection)
    try:
        yield cursor
    finally:
        await cursor.close()
        #await client.close()
