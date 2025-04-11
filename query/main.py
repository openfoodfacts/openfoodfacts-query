"""Starts FastAPI and the import scheduler and defines all of the API routes"""

import logging
from contextlib import asynccontextmanager
from importlib.metadata import metadata
from typing import Dict, List

from fastapi import FastAPI, Query

from query.database import get_transaction
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
    async with get_transaction() as transaction:
        await migrate_database(transaction)

    async with redis_lifespan():
        with scheduler_lifespan():
            yield
            logger.info("Shutting down")


package_metadata = metadata("query")
app = FastAPI(
    lifespan=lifespan,
    title=package_metadata["summary"],
    license_info={"name": package_metadata["license"]},
    version=package_metadata["version"],
)


@app.get("/health", response_model_exclude_none=True)
async def get_health() -> Health:
    """Get the health of the service and its dependencies"""
    return await check_health()


obsolete_param = Query(False, description="Whether to just search obsolete products")


@app.post("/count")
async def count(filter: Filter, obsolete: bool = obsolete_param) -> int:
    """Count the total number of products meeting the specified filter criteria"""
    return await query.count(filter, obsolete)


@app.post("/aggregate")
async def aggregate(
    stages: List[Stage], obsolete: bool = obsolete_param
) -> List[AggregateResult] | AggregateCountResult:
    """Get the aggregate count of products by the specified grouping field. If a $count stage is supplied then the count of distinct group values will be returned"""
    return await query.aggregate(stages, obsolete)


@app.post("/find")
async def find(
    find_query: FindQuery,
    obsolete: bool = obsolete_param,
) -> List[Dict]:
    """Fetch the specified product documents"""
    return await query.find(find_query, obsolete)


@app.get("/importfrommongo")
async def importfrommongo(
    start_from: str = Query(
        None,
        alias="from",
        description="The last updated date from which to import products. A full import will be performed if this is not supplied. Supply but leave blank to import products updated since the last import",
    )
):
    """Runs a full or incremental import from MongoDB"""
    return await ingestion.import_from_mongo(start_from)


@app.post("/scans")
async def scans(
    scans: ProductScans,
    fullyloaded: bool = Query(
        False,
        description="Set to true when all scans are loaded and popularity queries can now be supported",
    ),
):
    """Used for bulk loading product scan data from logs"""
    await import_scans(scans, fullyloaded)
