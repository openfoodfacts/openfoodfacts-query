from typing import List
from asyncpg import Connection


async def create_table(connection):
    await connection.execute(
        """CREATE TABLE IF NOT EXISTS contributor (
      id serial,
      code text,
      constraint contributor_pkey primary key (id),
      constraint contributor_code unique (code))"""
    )

async def create_contributors_from_events(connection: Connection, event_ids: List[int]):
    await connection.execute("""insert into contributor (code)
      select distinct message->>'user_id'
      from product_update_event 
      where id = ANY($1)
      and not exists (select * from contributor where code = message->>'user_id')
      on conflict (code)
      do nothing""", event_ids)
