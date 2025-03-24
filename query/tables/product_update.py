from typing import List

from asyncpg import Connection


async def create_table(connection: Connection):
    await connection.execute(
        """CREATE TABLE IF NOT EXISTS product_update (
	    product_id int,
	    revision int,
      updated_date date,
      update_type_id int,
      contributor_id int,
      event_id bigint,
     constraint product_update_pkey primary key (product_id, revision))"""
    )
    await connection.execute(
        "create index product_update_updated_date_index on product_update (updated_date);"
    )

async def create_updates_from_events(connection: Connection, event_ids: List[int]):
    await connection.execute("""insert into contributor (code)
      select distinct message->>'user_id'
      from product_update_event 
      where id = ANY($1)
      and not exists (select * from contributor where code = message->>'user_id')
      on conflict (code)
      do nothing""", event_ids)

    await connection.execute("""insert into update_type (code)
      select distinct message->>'action'
      from product_update_event 
      where id = ANY($1)
      and not exists (select * from update_type where code = message->>'action')
      on conflict (code)
      do nothing""", event_ids)
    
    # Update counts on product_update after products have been imported
    # Note coalesce on rev is only needed for transition if an older version of PO is deployed
    await connection.execute("""INSERT INTO product_update (
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
      on conflict (product_id,revision) DO NOTHING""", event_ids)

