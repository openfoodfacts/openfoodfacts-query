from typing import List

from query.models.domain_event import DomainEvent
from query.models.product import Source
from query.services.ingestion import import_with_filter
from query.tables.product_update_event import create_events


async def process_events(transaction, events: List[DomainEvent]):
    await create_events(transaction, events)
    product_codes = [
        event.payload["code"]
        for event in events
        if event.payload.get("product_type") == "food"
    ]
    if product_codes:
        await import_with_filter(
            transaction, {"code": {"$in": product_codes}}, Source.event
        )
