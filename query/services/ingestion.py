"""Routines for importing product data from MongoDB"""

import logging
import math
from datetime import datetime, timezone
from typing import Dict

from asyncpg import Connection
from uvicorn.logging import TRACE_LOG_LEVEL
import asyncpg

from query.tables.product_nutrient import (
    NUTRIENT_TAG,
    NUTRITION_TAG,
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
from ..tables.settings import (
    get_last_updated,
    set_last_updated,
    set_pre_migration_message_id,
)

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

        # Keep a note of the last message id at the start of the upgrade as we want to re-play any messages
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
    # Commit the temporary table so it isn't rolled back on failure. Stays active for the session
    await transaction.execute("COMMIT")
    await transaction.execute("BEGIN TRANSACTION")

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
        # Cater for new nutrition structure
        if NUTRIENT_TAG in tags:
            projection |= {NUTRITION_TAG: True}

        for obsolete in [False, True]:
            update_count = 0
            skip_count = 0
            product_updates = []
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

                    # Strip any nulls from tag text. Note new nutrition schema doesn't allow ad-hoc entries so should not have this problem
                    for tag in list(TAG_TABLES.keys()) + [NUTRIENT_TAG]:
                        tag_data = product_data.get(tag, None)
                        strip_nuls(tag_data, f"Product: {product_code}, tag: {tag}")

                    product_updates.append(
                        [existing_product["id"], last_updated, product_data]
                    )

                    update_count += 1
                    if not (update_count % batch_size):
                        await apply_product_updates(
                            transaction,
                            product_updates,
                            obsolete,
                            process_id,
                            source,
                            tags,
                        )

            # Apply any remaining staged changes
            if update_count % batch_size:
                await apply_product_updates(
                    transaction,
                    product_updates,
                    obsolete,
                    process_id,
                    source,
                    tags,
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


async def apply_product_updates(
    transaction: Connection,
    product_updates,
    obsolete,
    process_id,
    source,
    tags,
):
    """Inserts data from product_updates into the the product_temp temporary table
    and then copies from here to the relational tables.
    Assumes that a minimal product record has already been created"""

    # It is possible that some products will have bad data that we have not anticipated in our SQL which may
    # cause one of the batch SQL statements to fail. In this case we want to isolate the problem product(s)
    # but still process the updates for the other products in the batch.
    # We use an optimistic model where we assume most products will pass, and also assume that errors will be
    # repeated, i.e. are not transient. The essence of the retry logic is as follows:
    # 1. If a batch fails then split the batch in two and try the first half again
    # 2. If the first half fails, repeat the process for the first half until we have isolated the problem product.
    #    If the first half succeeds, assume we have an error in the remaining half so split this again and repeat
    # 3. Once the problem product is isolated then assume all remaining products are OK and retry all of these together

    remaining_updates = []
    # max_fail_index as a pointer to the last possible item that could have an error
    # The index includes both product_updates (batch currently being tried) and remaining_updates
    max_fail_index = len(product_updates)
    retrying = False
    while len(product_updates):
        try:
            await transaction.executemany(
                """INSERT INTO product_temp (id, last_updated, data) 
                values ($1, $2, $3) ON CONFLICT DO NOTHING""",
                product_updates,
            )

            # Analyze the temp table first as this improves the generated query plans
            await transaction.execute("ANALYZE product_temp")

            if retrying:
                # We have to re-create any minimal products as they will have been rolled back
                # if we have had an error in this batch
                await transaction.execute(
                    """INSERT INTO product (id, code)
                    SELECT id, data->>'code'
                    FROM product_temp pt
                    WHERE NOT EXISTS (SELECT * FROM product p WHERE p.id = pt.id)"""
                )

            # Use the uvicorn TRACE log level for detailed ingestion logs
            log = lambda msg: logger.log(TRACE_LOG_LEVEL, msg)
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

            product_count = len(product_updates)
            logger.info(
                f"Imported {product_count}{' obsolete' if obsolete else ''} products"
            )
            del product_updates[:]

            if len(remaining_updates):
                # Reduce the max fail index by the number of products we've just succeeded with
                max_fail_index -= product_count
                # Split the remaining products in half. Where there is an odd number we want to retry
                # the larger part so that we always retry the last one
                # We still retry the last one even if we know all others have succeeded 
                # just in case the problem was transient
                retry_point = (max_fail_index + 1) // 2
                product_updates = remaining_updates[:retry_point]
                del remaining_updates[:retry_point]

        except asyncpg.PostgresError as sql_error:
            await transaction.execute("ROLLBACK")
            if len(product_updates) == 1:
                # We have found our bad product
                logger.error(
                    f"Error updating product: {product_updates[0][2]['code']}, {repr(sql_error)}"
                )
                del product_updates[:]
                product_updates.extend(remaining_updates)
                del remaining_updates[:]
                # Assume all the remaining products are OK (unless we get another failure)
                max_fail_index = len(product_updates)
            else:
                # We know that the failing product is in this batch
                max_fail_index = len(product_updates)
                
                # Split the products in half. Where there is an odd number we want to retry
                # the larger part so that we always retry the last one
                retry_point = (max_fail_index + 1) // 2
                # Move the second half to the beginning of the remaining_updates list
                remaining_updates[0:0] = product_updates[retry_point:]
                del product_updates[retry_point:]

            # Start a new transaction
            await transaction.execute("BEGIN TRANSACTION")
            retrying = True


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
