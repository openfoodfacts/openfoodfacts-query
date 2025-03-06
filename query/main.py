from contextlib import asynccontextmanager
import logging
from typing import Annotated, Any, Dict, Optional
import typing

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field, create_model

from query.db import Database
from query.migrator import migrate_database
from query.models.query import Filter
from query.models.health import Health
from query.services import query
from query.services.health import check_health
from query.tables.product_tags import tag_tables

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run migrations
    async with Database() as conn:
        await migrate_database(conn)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health", response_model_exclude_none=True)
async def get_health() -> Health:
    return await check_health()

@app.post("/count")
async def post_count(filter: Filter, obsolete: bool = False) -> int:
    return await query.count(filter, obsolete)

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

