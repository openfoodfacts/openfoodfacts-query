async def create_table(connection):
    await connection.execute(
        'create table settings (id serial primary key, last_updated timestamptz null, last_message_id text null);',
    )
