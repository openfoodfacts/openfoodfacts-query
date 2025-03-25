from typing import Dict
from query.database import database_connection
from query.models.scan import ScanCounts, ProductScans
from query.tables.loaded_tag import append_loaded_tags
from query.tables.product_country import PRODUCT_COUNTRY_TAG
from query.tables.product_scans_by_country import create_scans


async def import_scans(scans: ProductScans, fully_loaded = False):
    async with database_connection() as connection:
        await create_scans(connection, scans)

        if fully_loaded:
            await append_loaded_tags(connection, [PRODUCT_COUNTRY_TAG]);
