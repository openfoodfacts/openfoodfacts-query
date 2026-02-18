"""Routines that operate on product scan data. Scans are currently just loaded in a batch from logs
but will hopefully be loaded from events in the future"""

from query.tables.product_scans import insert_product_scans

from ..database import get_transaction
from ..models.scan import ProductScans
from ..tables.loaded_tag import append_loaded_tags
from ..tables.product import PRODUCT_SCANS_TAG, fixup_product_scans, normalize_code
from ..tables.product_country import (
    PRODUCT_COUNTRY_TAG,
    fixup_product_country_scans,
)
from ..tables.product_scans_by_country import insert_product_scans_by_country


async def import_scans(scans: ProductScans, fully_loaded=False):
    """Imports batches of product scans (currently generated from logs).
    The caller should set the fully_loaded flag on the last batch which will then
    enable support for popularity based queries"""
    async with get_transaction() as transaction:
        # The PO import routine sends the directory name as the product code, so we need to normalize it
        normalized_scans = ProductScans.model_validate({})
        for code in scans.root.keys():
            product_scans = scans.root[code]
            normalized_scans.root[normalize_code(code)] = product_scans
            # Also may send gb as a synonym for uk. Fix this here
            for scans_counts in product_scans.root.values():
                gb_scans = scans_counts.unique_scans_n_by_country.root.get("gb")
                if gb_scans:
                    scans_counts.unique_scans_n_by_country.root["uk"] = (
                        gb_scans
                        + scans_counts.unique_scans_n_by_country.root.get("uk", 0)
                    )

        await insert_product_scans_by_country(transaction, normalized_scans)
        await insert_product_scans(transaction, normalized_scans)

        if fully_loaded:
            await scans_fully_loaded(transaction)


async def get_current_scan_year(transaction):
    """Work out the current year for popularity sorting.
    Tests should mock this to return TEST_YEAR"""
    return await transaction.fetchval("""select max(year) from product_scans""")


async def scans_fully_loaded(transaction):
    current_year = await get_current_scan_year(transaction)
    oldest_year = current_year - 5
    await fixup_product_country_scans(transaction, current_year, oldest_year)
    await fixup_product_scans(transaction, current_year)
    await append_loaded_tags(transaction, [PRODUCT_COUNTRY_TAG, PRODUCT_SCANS_TAG])
