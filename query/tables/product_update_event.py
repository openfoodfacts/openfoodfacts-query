async def create_table(connection):
    await connection.execute(
        """CREATE TABLE IF NOT EXISTS product_update_event (
      id bigserial NOT NULL PRIMARY KEY,
      message_id text NOT NULL,
      received_at timestamptz NOT NULL,
      updated_at timestamptz NOT NULL,
      message jsonb NOT NULL)"""
    )
