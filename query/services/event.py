"""Business logic for processing domain events"""

import math
from datetime import datetime, timezone
from typing import Dict, List

from query.database import get_transaction, strip_nuls

from ..models.domain_event import DomainEvent
from ..models.product import Source
from ..services.ingestion import import_with_filter
from ..tables.product_update_event import create_events

STREAM_NAME = "product_updates"


async def process_events(transaction, events: List[DomainEvent]):
    """Process events received from Redis"""
    await create_events(transaction, events)
    product_codes = [
        event.payload["code"]
        for event in events
        # We only currently support events for food products.
        # TODO: This logic should be inside the import so we can delete non-food products
        if event.payload.get("product_type") == "food"
    ]
    if product_codes:
        await import_with_filter(
            transaction, {"code": {"$in": product_codes}}, Source.event
        )


async def import_events(payloads: List[Dict]):
    """Bulk load historic events without triggering a product import"""
    events: List[DomainEvent] = []
    for payload in payloads:
        """Determine the time that the domain event took place"""
        try:
            # Use the timestamp property on the message payload if it is provided
            timestamp = datetime.fromtimestamp(payload["timestamp"], timezone.utc)
        except:
            # If all else fails use the current time
            timestamp = datetime.now(timezone.utc)

        # Always ensure we have a unique message id
        message_id = (
            f"{math.floor(timestamp.timestamp())}-{payload.get('code')}-{payload.get('rev')}"
        )
        strip_nuls(payload, f"import_event {message_id}")
        events.append(
            DomainEvent(
                id=message_id, timestamp=timestamp, type=STREAM_NAME, payload=payload
            )
        )

    async with get_transaction() as transaction:
        event_ids = await create_events(transaction, events)
        
    return event_ids
