"""A leaner version of the product update events, used to support queries more efficiently"""

from typing import List

from asyncpg import Connection

from query.tables.contributor import create_contributors_from_events
from query.tables.update_type import create_update_types_from_events


async def create_table(transaction: Connection):
    await transaction.execute(
        """CREATE TABLE IF NOT EXISTS product_update (
	    product_id int,
	    revision int,
      updated_date date,
      update_type_id int,
      contributor_id int,
      event_id bigint,
     constraint product_update_pkey primary key (product_id, revision))"""
    )
    await transaction.execute(
        "create index product_update_updated_date_index on product_update (updated_date);"
    )


async def create_updates_from_events(transaction: Connection, event_ids: List[int]):
    await create_contributors_from_events(transaction, event_ids)

    await create_update_types_from_events(transaction, event_ids)

    # Update counts on product_update after products have been imported
    # Note coalesce on rev is only needed for transition if an older version of PO is deployed
    await transaction.execute(
        """INSERT INTO product_update (
        product_id,
        revision,
        updated_date,
        update_type_id,
        contributor_id,
        event_id)
      SELECT 
      	p.id,
        coalesce((pe.message->>'rev')::int, p.revision),
        date(pe.updated_at at time zone 'UTC') updated_day,
        update_type.id,
        contributor.id,
        pe.id
      FROM product_update_event pe
        JOIN product p on p.code = pe.message->>'code'
        join contributor on contributor.code = pe.message->>'user_id'
        join update_type on update_type.code = pe.message->>'action'
      where pe.id = ANY($1)
      on conflict (product_id,revision) DO NOTHING""",
        event_ids,
    )
