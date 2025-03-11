from contextlib import asynccontextmanager
import logging
from typing import List
from fastapi import FastAPI

from query.database import database_connection
from query.migrator import migrate_database
from query.models.query import AggregateCountResult, AggregateResult, Filter, Stage
from query.models.health import Health
from query.services import query
from query.services.health import check_health

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_):
    # Run migrations
    async with database_connection() as conn:
        await migrate_database(conn)
    yield


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
