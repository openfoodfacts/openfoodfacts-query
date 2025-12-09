"""The raw event data for each product_updated event"""

from datetime import datetime, timezone
from typing import List

from asyncpg import Connection

from ..models.domain_event import DomainEvent
from ..tables.product_update import create_updates_from_events


async def create_table(transaction):
    await transaction.execute(
        """CREATE TABLE IF NOT EXISTS product_update_event (
      id bigserial NOT NULL PRIMARY KEY,
      message_id text NOT NULL,
      received_at timestamptz NOT NULL,
      updated_at timestamptz NOT NULL,
      message jsonb NOT NULL)"""
    )


async def add_message_id_constraint(transaction):
    # Create a temporary index so the following updates run faster
    await transaction.execute(
        "CREATE INDEX product_update_event_temp ON product_update_event (message_id)"
    )

    # Make sure product_updates are pointing to the earliest version of an event
    await transaction.execute(
        """UPDATE product_update SET event_id = 
        (SELECT min(id) FROM product_update_event WHERE message_id = 
        (SELECT message_id FROM product_update_event WHERE id = event_id))"""
    )

    # Remove any later duplicates
    await transaction.execute(
        """DELETE FROM product_update_event pue WHERE
        EXISTS (SELECT * FROM product_update_event pue2 WHERE pue2.id < pue.id AND pue2.message_id = pue.message_id)"""
    )

    # Add constraint
    await transaction.execute(
        """ALTER TABLE product_update_event ADD CONSTRAINT message_id UNIQUE (message_id)"""
    )

    # Drop temporary index
    await transaction.execute("DROP INDEX product_update_event_temp")


async def create_events(transaction: Connection, events: List[DomainEvent]):
    received_at = datetime.now(timezone.utc)
    
    results = await transaction.fetchmany(
        """INSERT into product_update_event (message_id, received_at, updated_at, message) VALUES ($1, $2, $3, $4)
        ON CONFLICT (message_id) DO NOTHING
        RETURNING id""",
        [[event.id, received_at, event.timestamp, event.payload] for event in events],
    )

    event_ids = [result["id"] for result in results]
    await create_updates_from_events(transaction, event_ids)
    return event_ids
