from contextlib import asynccontextmanager
from enum import Enum
import logging
from typing import Dict, Union
import typing

from fastapi import FastAPI
from pydantic import BaseModel, Field, create_model
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis

from query.db import Database, settings
from query.migrator import migrate_database
from query.tables.product_tags import tag_tables

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run migrations
    async with Database() as conn:
        await migrate_database(conn)
    yield


app = FastAPI(lifespan=lifespan)


class HealthStatusEnum(str, Enum):
    ok = "ok"
    error = "error"


class HealthItemStatusEnum(str, Enum):
    up = "up"
    down = "down"


class HealthItem(BaseModel):
    status: HealthItemStatusEnum = HealthItemStatusEnum.up
    reason: str | None = None


class Health(BaseModel):
    def add(self, name: str, status: HealthItemStatusEnum, reason: str = None):
        self.info[name] = HealthItem(status=status, reason=reason)
        if status != HealthItemStatusEnum.up:
            self.status = HealthStatusEnum.error

    status: HealthStatusEnum = HealthStatusEnum.ok
    info: Dict[str, HealthItem] = dict()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health", response_model_exclude_none=True)
async def health() -> Health:
    health = Health()

    try:
        async with Database() as conn:
            await conn.fetch("SELECT 1 FROM product LIMIT 1")
        health.add("postgres", HealthItemStatusEnum.up)
    except Exception as e:
        health.add("postgres", HealthItemStatusEnum.down, str(e))

    try:
        client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=1000)
        await client.admin.command("ping")
        health.add("mongodb", HealthItemStatusEnum.up)
    except Exception as e:
        health.add("mongodb", HealthItemStatusEnum.down, str(e))

    try:
        redis_client = redis.Redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        health.add("redis", HealthItemStatusEnum.up)
    except Exception as e:
        health.add("redis", HealthItemStatusEnum.down, str(e))

    # TODO: Should maybe throw and exception here and format with a custom exception handler: https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
    return health

# Test to see if we can define a strict model for queries
# Tried namedtuple but that didn't seem to work
keys = {key.replace('_', '-'): (str, Field(alias=key, default=None,  exclude=None)) for key in tag_tables.keys()}
keys['$and'] = (str | None, None)
# The type checker can't cope with a dynamic model so skip that here
if typing.TYPE_CHECKING:
    # TODO: Come up with a more generic model for type checking
    Find = BaseModel
else:
    Find = create_model('Find', **keys)

@app.post("/test", response_model_exclude_none=True)
async def test(find: Find):
    return find