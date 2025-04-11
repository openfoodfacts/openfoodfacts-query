"""The kind of product update that was performed. Used when recording product_update events"""

from typing import List

from asyncpg import Connection


async def create_table(transaction):
    await transaction.execute(
        """CREATE TABLE IF NOT EXISTS update_type (
      id serial,
      code text,
      constraint action_pkey primary key (id),
      constraint action_code unique (code))"""
    )

    await transaction.execute(
        """INSERT INTO update_type (code) VALUES ('created'), ('updated'), ('archived'), ('unarchived'), ('deleted'), ('reprocessed'), ('unknown')"""
    )


async def create_update_types_from_events(
    transaction: Connection, event_ids: List[int]
):
    await transaction.execute(
        """insert into update_type (code)
      select distinct message->>'action'
      from product_update_event 
      where id = ANY($1)
      and not exists (select * from update_type where code = message->>'action')
      on conflict (code)
      do nothing""",
        event_ids,
    )
