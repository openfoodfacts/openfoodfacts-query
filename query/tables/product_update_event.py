from datetime import datetime, timezone
from typing import List

from asyncpg import Connection

from query.models.domain_event import DomainEvent
from query.tables.product_update import create_updates_from_events


async def create_table(transaction):
    await transaction.execute(
        """CREATE TABLE IF NOT EXISTS product_update_event (
      id bigserial NOT NULL PRIMARY KEY,
      message_id text NOT NULL,
      received_at timestamptz NOT NULL,
      updated_at timestamptz NOT NULL,
      message jsonb NOT NULL)"""
    )


async def create_events(transaction: Connection, events: List[DomainEvent]):
    received_at = datetime.now(timezone.utc)
    results = await transaction.fetchmany(
        "INSERT into product_update_event (message_id, received_at, updated_at, message) VALUES ($1, $2, $3, $4) RETURNING id",
        [[event.id, received_at, event.timestamp, event.payload] for event in events],
    )

    event_ids = [result["id"] for result in results]
    await create_updates_from_events(transaction, event_ids)
    return event_ids
