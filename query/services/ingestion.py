"""Routines for importing product data from MongoDB"""

import logging
import math
from datetime import datetime, timezone
from typing import Dict

from asyncpg import Connection

from query.tables.product_nutrient import (
    NUTRIENT_TAG,
    create_product_nutrients_from_staging,
)

from ..config import config_settings
from ..database import get_transaction, strip_nuls
from ..models.product import Source
from ..mongodb import find_products
from ..tables.product import (
    PRODUCT_FIELD_COLUMNS,
    PRODUCT_TAG,
    create_minimal_product,
    delete_products,
    get_minimal_product,
    update_products_from_staging,
)
from ..tables.product_country import fixup_product_countries
from ..tables.product_ingredient import (
    INGREDIENTS_TAG,
    create_ingredients_from_staging,
)
from ..tables.product_tags import COUNTRIES_TAG, TAG_TABLES, create_tags_from_staging
from ..tables.settings import get_last_updated, set_last_updated, set_pre_migration_message_id

logger = logging.getLogger(__name__)

MIN_DATETIME = datetime(1, 1, 1, tzinfo=timezone.utc)
DEFAULT_BATCH_SIZE = 10000


async def get_process_id(transaction):
    """Provides a unique identifier for the transaction.
    Used during a full load to delete products that don't have the identifier once the load is complete
    """
    return await transaction.fetchval("SELECT pg_current_xact_id()")


def int_or_none(value):
    return None if value == None else int(value)


def get_product_last_updated(product_data):
    """Get the last updated date for a product as a datetime.
    Falls back to last_modified_t if last_updated_t is not available"""
    try:
        last_updated = datetime.fromtimestamp(
            product_data.get(
                "last_updated_t",
                product_data.get("last_modified_t"),
            ),
            timezone.utc,
        )
    except TypeError:
        logger.warning(
            f"Product: {product_data['code']}. Invalid last_updated_t: {product_data.get('last_updated_t')}, or last_modified_t: {product_data.get('last_modified_t')}."
        )
        last_updated = MIN_DATETIME

    return last_updated


async def import_with_filter(
    transaction,
    filter: Dict,
    source: Source,
    batch_size=DEFAULT_BATCH_SIZE,
    tags=[],
) -> datetime:
    """Core import routine. Fetches data from MongoDB using the supplied filter and updates the copy stored in PostgreSQL
    If the filter is a list of codes then any code not found in MongoDB will be deleted from PostgreSQL
    """

    max_last_updated = MIN_DATETIME
    found_product_codes = []
    codes_specified = "code" in filter and "$in" in filter["code"]
    if tags:
        # If explicit tags are provided then this is a partial load
        source = Source.partial

        # Partial loads are done during migrations but we don't want to do these during tests
        if config_settings.SKIP_DATA_MIGRATIONS:
            return

        # Keep a not of the last message id at the start of the upgrade as we want to re-play any messages
        # that were processed by the old version after this point
        await set_pre_migration_message_id()
    else:
        tags = list(TAG_TABLES.keys()) + [INGREDIENTS_TAG, PRODUCT_TAG, NUTRIENT_TAG]

    # We currently use a temporary table to stage the unstructured product data to minimize overall storage
    # Ideally this would be a permanent table so that we can easily extend the relational model without having
    # to do a full import
    await transaction.execute(
        "CREATE TEMP TABLE product_temp (id int PRIMARY KEY, last_updated timestamptz, data jsonb)"
    )
    try:
        process_id = await get_process_id(transaction)
        projection = {key: True for key in tags if key != PRODUCT_TAG}
        # Add specific fields for top-level product fields
        if PRODUCT_TAG in tags:
            projection |= {key: True for key in PRODUCT_FIELD_COLUMNS.keys()}
        else:
            # If we aren't updating the product then just fetch the code and dates
            projection |= {
                "code": True,
                "last_modified_t": True,
                "last_updated_t": True,
            }

        for obsolete in [False, True]:
            update_count = 0
            skip_count = 0
            async with find_products(filter, projection, obsolete) as cursor:
                async for product_data in cursor:
                    product_code = product_data["code"]
                    existing_product = await get_minimal_product(
                        transaction, product_code
                    )
                    # Don't create new products for partial updates
                    if not existing_product and source == Source.partial:
                        continue

                    last_updated = get_product_last_updated(product_data)
                    max_last_updated = max(last_updated, max_last_updated)

                    if codes_specified:
                        found_product_codes.append(product_code)

                    # Don't update the product if we are doing an incremental load and the product hasn't changed.
                    # This way we should see most products with a Source of "event" and any product with a source of
                    # "incremental_load" would indicate there was a scenario where an event wasn't generated
                    if (
                        existing_product
                        and source == Source.incremental_load
                        and existing_product["last_updated"] == last_updated
                    ):
                        skip_count += 1
                        if not (skip_count % batch_size):
                            logger.info(
                                f"Skipped {skip_count}{' obsolete' if obsolete else ''} products"
                            )
                        continue

                    if not existing_product:
                        existing_product = await create_minimal_product(
                            transaction, product_code
                        )

                    # Strip any nulls from tag text
                    for tag in list(TAG_TABLES.keys()) + [NUTRIENT_TAG]:
                        tag_data = product_data.get(tag, None)
                        strip_nuls(tag_data, f"Product: {product_code}, tag: {tag}")
                    

                    await transaction.execute(
                        "INSERT INTO product_temp (id, last_updated, data) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
                        existing_product["id"],
                        last_updated,
                        product_data,
                    )

                    update_count += 1
                    if not (update_count % batch_size):
                        await apply_staged_changes(
                            transaction,
                            obsolete,
                            update_count,
                            process_id,
                            source,
                            tags,
                        )

            # Apply any remaining staged changes
            if update_count % batch_size:
                await apply_staged_changes(
                    transaction, obsolete, update_count, process_id, source, tags
                )
            if skip_count % batch_size:
                logger.info(
                    f"Skipped {skip_count}{' obsolete' if obsolete else ''} products"
                )

        # Mark all products specifically requested but not found as deleted
        if codes_specified:
            requested_product_codes = filter["code"]["$in"]
            missing_product_codes = [
                code
                for code in requested_product_codes
                if code not in found_product_codes
            ]
            if missing_product_codes:
                await delete_products(
                    transaction, process_id, source, missing_product_codes
                )

        # If this is a full load then delete all products that were not fetched from MongoDB on this run
        if source == Source.full_load:
            await delete_products(transaction, process_id, source)
    finally:
        await transaction.execute("DROP TABLE product_temp")

    return max_last_updated


async def apply_staged_changes(
    transaction: Connection, obsolete, update_count, process_id, source, tags
):
    """ "Copies data from the product_temp temporary table to the relational tables.
    Assumes that a basic product record has already been created"""
    # Analyze the temp table first as this improves the generated query plans
    await transaction.execute("ANALYZE product_temp")

    log = logger.debug
    if PRODUCT_TAG in tags:
        await update_products_from_staging(
            transaction, log, obsolete, process_id, source
        )

    if INGREDIENTS_TAG in tags:
        await create_ingredients_from_staging(transaction, log, obsolete)

    await create_tags_from_staging(transaction, log, obsolete, tags)

    if COUNTRIES_TAG in tags:
        await fixup_product_countries(transaction, obsolete)

    if NUTRIENT_TAG in tags:
        await create_product_nutrients_from_staging(transaction, log)

    await transaction.execute("TRUNCATE TABLE product_temp")

    # Start a new transaction for the next batch
    # The calling process will commit the final transaction
    await transaction.execute("COMMIT")
    await transaction.execute("BEGIN TRANSACTION")

    logger.info(f"Imported {update_count}{' obsolete' if obsolete else ''} products")


import_running = False


async def import_from_mongo(from_date: str = None):
    """Imports data from MongoDB that has been updated since the date specified.
    If the date specified is None then full import is performed.
    If the date is empty then products updated since the last incremental import will be loaded
    """
    global import_running
    if import_running:
        logger.warning("Skipping as import already running")
        return

    import_running = True
    try:
        source = Source.full_load if from_date == None else Source.incremental_load
        async with get_transaction() as transaction:
            # If the from parameter is supplied but it is empty then obtain the most
            # recent modified time from the database and query MongoDB for products
            # modified since then
            if not from_date and source == Source.incremental_load:
                last_updated = await get_last_updated(transaction)
                if last_updated:
                    from_date = last_updated.isoformat()
                else:
                    # If we don't have a last_updated in the database then we are doing a full load
                    source = Source.full_load

            filter = {}
            if from_date:
                # Note in python the timestamp is in whole seconds (matches Perl)
                from_time = math.floor(datetime.fromisoformat(from_date).timestamp())
                filter["last_updated_t"] = {"$gt": from_time}
                logger.info(f"Starting import from {from_date}")

            max_last_updated = await import_with_filter(transaction, filter, source)
            if max_last_updated != MIN_DATETIME:
                await set_last_updated(transaction, max_last_updated)
    finally:
        import_running = False
