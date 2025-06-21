from query.models.product import Source
from query.services.ingestion import import_with_filter
from query.tables.product_nutrient import NUTRIENT_TAG


async def up(transaction):
    await import_with_filter(transaction, {}, Source.partial, tags=[NUTRIENT_TAG])
