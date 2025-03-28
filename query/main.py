import logging
from contextlib import asynccontextmanager
from typing import Dict, List

from fastapi import FastAPI, Query

from query.database import database_connection
from query.migrator import migrate_database
from query.models.health import Health
from query.models.query import (
    AggregateCountResult,
    AggregateResult,
    Filter,
    FindQuery,
    Stage,
)
from query.models.scan import ProductScans
from query.redis import redis_lifespan
from query.scheduler import scheduler_lifespan
from query.services import ingestion, query
from query.services.health import check_health
from query.services.scan import import_scans

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_):
    # Run migrations
    async with database_connection() as conn:
        await migrate_database(conn)

    async with redis_lifespan():
        with scheduler_lifespan():
            yield
            logger.info("Shutting down")


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


@app.post("/scans")
async def scans(scans: ProductScans, fullyloaded=False):
    await import_scans(scans, fullyloaded)
