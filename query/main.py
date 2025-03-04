from contextlib import asynccontextmanager
from enum import Enum
import logging
from typing import Annotated, Any, Dict, Optional, Union
import typing

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field, RootModel, constr, create_model, model_validator, root_validator
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

class Find(BaseModel):
    and_expression: Annotated[str, Field(alias='$and', default=None)]

    model_config = ConfigDict(extra='allow')

    __pydantic_extra__: Dict[str, Any] = Field(init=False)

# The type checker can't cope with a dynamic model so skip that here
if not typing.TYPE_CHECKING:
    keys = {key.replace('_', '-'): (Optional[str], Field(alias=key, default=None)) for key in tag_tables.keys()}
    keys['model_config'] = (ConfigDict(extra='forbid'))
    Find = create_model('Find', __base__ = Find, **keys)

@app.post("/test")
async def test(find: Find):
    return find.model_dump(exclude_defaults=True)

