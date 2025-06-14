"""Routines that operate on product scan data. Scans are currently just loaded in a batch from logs
but will hopefully be loaded from events in the future"""

from ..database import get_transaction
from ..models.scan import ProductScans
from ..tables.loaded_tag import append_loaded_tags
from ..tables.product import PRODUCT_SCANS_TAG, normalize_code, update_scans
from ..tables.product_country import (
    PRODUCT_COUNTRY_TAG,
    fixup_product_countries_for_products,
)
from ..tables.product_scans_by_country import create_scans


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

        ids_updated = await update_scans(transaction, normalized_scans)
        await create_scans(transaction, normalized_scans)
        if ids_updated:
            await fixup_product_countries_for_products(transaction, ids_updated)

        if fully_loaded:
            await append_loaded_tags(
                transaction, [PRODUCT_COUNTRY_TAG, PRODUCT_SCANS_TAG]
            )
