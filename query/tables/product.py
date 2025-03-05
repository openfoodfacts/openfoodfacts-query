from asyncpg import Connection, Record


async def create_table(connection: Connection):
    await connection.execute(
        'create table product (id serial not null, name text null, code text null, last_updated timestamptz null, creator text null, owners_tags text null, obsolete boolean null default false, ingredients_without_ciqual_codes_count int null, ingredients_count int null, last_processed timestamptz null, source varchar(255) null, revision int null, process_id bigint null, constraint product_pkey primary key (id));',
    )
    await connection.execute(
        'create index product_code_index on product (code);',
    )
    await connection.execute(
        'create index product_process_id_index on product (process_id);'
    )
    await connection.execute(
        'create index product_creator_index on product (creator);'
    )
    await connection.execute(
        'create index product_owners_tags_index on product (owners_tags);'
    )

async def create_product(connection: Connection, code):
    record = await connection.fetchrow('INSERT INTO product (code) VALUES ($1) RETURNING id', code)
    return record['id']
