"""Runs scheduled (cron) tasks. Currently just an incremental import from MongoDB every evening.
In theory this should not be needed except for running a full import when support for new tags has
been added but these have not yet been loaded into PostgreSQL. If we see any products with a source
of 'incremental_load' then this may indicate a scenario where a product is being updated without
generating a Redis event, which should be investigated"""

import logging
from contextlib import contextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .database import get_transaction
from .events import start_redis_listener, stop_redis_listener
from .services.ingestion import import_from_mongo
from .tables.loaded_tag import get_loaded_tags
from .tables.product_tags import TAG_TABLES

logger = logging.getLogger(__name__)


async def scheduled_import_from_mongo():
    """Run an incremental import from MongoDB. Converts to a full import if more scan tables have been added since the last run"""
    async with get_transaction() as transaction:
        try:
            # Pause redis while we are importing
            await stop_redis_listener()
            loaded_tags = await get_loaded_tags(transaction)
            # If every tag is loaded then we do an incremental import. otherwise full
            if any(tag for tag in TAG_TABLES.keys() if tag not in loaded_tags):
                logger.info("Scheduled full import started")
                await import_from_mongo()
            else:
                logger.info("Scheduled incremental import started")
                await import_from_mongo("")
        finally:
            start_redis_listener()


@contextmanager
def scheduler_lifespan():
    """Starts and stops the scheduler with FastAPI"""
    scheduler = AsyncIOScheduler()
    try:
        scheduler.start()
        # Run at 2am every evening
        scheduler.add_job(scheduled_import_from_mongo, "cron", hour=2)
        yield
    finally:
        scheduler.shutdown()
