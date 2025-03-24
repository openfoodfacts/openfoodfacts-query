from typing import List

from query.database import database_connection
from query.models.domain_event import DomainEvent
from query.models.product import Source
from query.services.ingestion import import_with_filter
from query.tables.product_update_event import create_events


async def process_events(events: List[DomainEvent]):
    async with database_connection() as connection:
        await create_events(connection, events)
        product_codes = [event.payload['code'] for event in events if event.payload.get('product_type') == 'food']
        if product_codes:
            await import_with_filter({"code": {"$in": product_codes}}, Source.event)