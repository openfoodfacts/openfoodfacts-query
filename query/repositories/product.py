async def create_table(connection):
    await connection.execute(
        'create table "product" ("id" uuid not null, "data" jsonb null, "name" text null, "code" text null, "last_modified" timestamp null, "creator" text null, "owners_tags" text null, "last_update_id" uuid null, "obsolete" boolean not null default false, constraint "product_pkey" primary key ("id"));',
    )
    await connection.execute(
        'create index "product_code_index" on "product" ("code");',
    )
    await connection.execute(
        'create index "product_last_update_id_index" on "product" ("last_update_id");',
    )
    await connection.execute(
        'ALTER TABLE query.product ALTER COLUMN "data" TYPE json USING "data"::text::json;',
    )

    await connection.execute(
        'alter table "product" add column "ingredients_without_ciqual_codes_count" int null, add column "ingredients_count" int null;',
    )
    await connection.execute(
        'alter table "product" add column "last_updated" timestamp null, add column "source" varchar(255) null;',
    )
    # Merged in from a later migration
    await connection.execute('alter table "product" drop column "data";')

async def drop_pkey(connection):
    await connection.execute(
        'ALTER TABLE "product" DROP CONSTRAINT product_pkey CASCADE;'
    )
    await connection.execute('alter table "product" RENAME COLUMN "id" TO "old_id";')
    await connection.execute(
        'CREATE UNIQUE INDEX product_old_id ON "product" (old_id);'
    )

    await connection.execute('alter table "product" add column "id" serial NOT NULL;')

    await connection.execute(
        'alter table "product" add constraint "product_pkey" primary key ("id");'
    )

async def drop_old_id(connection):
    await connection.execute("DROP INDEX query.product_old_id;")
    await connection.execute("alter table query.product drop column old_id;")

    await connection.execute(
        'alter table "product" alter column "last_modified" type timestamptz using ("last_modified"::timestamptz);'
    )
    await connection.execute(
        'alter table "product" alter column "last_updated" type timestamptz using ("last_updated"::timestamptz);'
    )

    await connection.execute(
        'alter table "product" add column "revision" int null;',
    )
    await connection.execute(
        'alter table "product" alter column "obsolete" type boolean using ("obsolete"::boolean);'
    )
    await connection.execute(
        'alter table "product" alter column "obsolete" drop not null;'
    )

    await connection.execute(
        'alter table "product" rename column "last_updated" to "last_processed";'
    )
    await connection.execute(
        'alter table "product" rename column "last_modified" to "last_updated";'
    )
    await connection.execute(
        'alter table "product" add column "process_id" bigint null;'
    )
    await connection.execute(
        'create index "product_process_id_index" on "product" ("process_id");'
    )
    await connection.execute('drop index "product_last_update_id_index";')
    await connection.execute('alter table "product" drop column "last_update_id";')


