async def create_table(connection):
    await connection.execute(
        """CREATE TABLE IF NOT EXISTS update_type (
      id serial,
      code text,
      constraint action_pkey primary key (id),
      constraint action_code unique (code))"""
    )

    await connection.execute(
        """INSERT INTO update_type (code) VALUES ('created'), ('updated'), ('archived'), ('unarchived'), ('deleted'), ('reprocessed'), ('unknown')"""
    )
