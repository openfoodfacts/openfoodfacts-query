from query.database import get_transaction
from query.models.scan import ProductScans
from query.tables.loaded_tag import append_loaded_tags
from query.tables.product import normalize_code
from query.tables.product_country import PRODUCT_COUNTRY_TAG
from query.tables.product_scans_by_country import create_scans


async def import_scans(scans: ProductScans, fully_loaded=False):
    async with get_transaction() as transaction:
        # The PO import routine sends the directory name as the product code, so we need to normalize it
        normalized_scans = ProductScans.model_validate({})
        for code in scans.root.keys():
            normalized_scans.root[normalize_code(code)] = scans.root[code]

        await create_scans(transaction, normalized_scans)

        if fully_loaded:
            await append_loaded_tags(transaction, [PRODUCT_COUNTRY_TAG])
