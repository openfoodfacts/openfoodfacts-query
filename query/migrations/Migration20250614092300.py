from query.models.product import Source
from query.services.ingestion import import_with_filter

from ..tables import product


async def up(transaction):
    await product.add_v2_columns(transaction)
    await import_with_filter(transaction, {}, Source.full_load, do_children=False)
