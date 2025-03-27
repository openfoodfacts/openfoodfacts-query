import asyncio
from contextlib import asynccontextmanager
import logging
from typing import Annotated, Dict, List
from fastapi import FastAPI, Query
from pydantic import Field

from query.database import database_connection
from query.migrator import migrate_database
from query.models.query import (
    AggregateCountResult,
    AggregateResult,
    Filter,
    FindQuery,
    Stage,
)
from query.models.health import Health
from query.models.scan import ScanCounts, ProductScans
from query.redis import redis_listener
from query.services import ingestion, query
from query.services.health import check_health
from query.services.scan import import_scans

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_):
    # Run migrations
    async with database_connection() as conn:
        await migrate_database(conn)

    redis_listener_task = asyncio.create_task(redis_listener())
    yield
    logger.info("Shutting down")
    redis_listener_task.cancel()
    try:
        await redis_listener_task
    except asyncio.CancelledError:
        logger.info("Redis cancelled successfully")
        pass


app = FastAPI(lifespan=lifespan)


@app.get("/health", response_model_exclude_none=True)
async def get_health() -> Health:
    return await check_health()


@app.post("/count")
async def count(filter: Filter, obsolete: bool = False) -> int:
    return await query.count(filter, obsolete)


@app.post("/aggregate")
async def aggregate(
    stages: List[Stage], obsolete: bool = False
) -> List[AggregateResult] | AggregateCountResult:
    return await query.aggregate(stages, obsolete)


@app.post("/find")
async def find(find_query: FindQuery, obsolete: bool = False) -> List[Dict]:
    return await query.find(find_query, obsolete)


@app.get("/importfrommongo")
async def importfrommongo(start_from: str = Query(None, alias="from")):
    return await ingestion.import_from_mongo(start_from)


# TODO: Get OpenAPI looking nicer
@app.post("/scans")
async def scans(scans: ProductScans, fullyloaded=False):
    await import_scans(scans, fullyloaded)
