from query.models.product import Source
from query.services.ingestion import import_with_filter

from ..tables import product
from ..config import config_settings


async def up(transaction):
    await product.add_v2_columns(transaction)
    if not config_settings.SKIP_DATA_MIGRATIONS:
        await import_with_filter(transaction, {}, Source.full_load, do_children=False)
