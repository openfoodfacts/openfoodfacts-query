from query.db import settings


async def up(connection):
    await connection.execute(
        """CREATE TABLE IF NOT EXISTS product_update_event (
      id bigserial NOT NULL PRIMARY KEY,
      message_id text NOT NULL,
      received_at timestamptz NOT NULL,
      updated_at timestamptz NOT NULL,
      message jsonb NOT NULL)"""
    )

    await connection.execute(
        """CREATE TABLE IF NOT EXISTS contributor (
      id serial,
      code text,
      constraint contributor_pkey primary key (id),
      constraint contributor_code unique (code))"""
    )

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

    await connection.execute("create schema if not exists views;")
    await connection.execute(
        f"""CREATE USER {settings.VIEW_USER} PASSWORD '{settings.VIEW_PASSWORD}'""")
    await connection.execute(
        f"""ALTER ROLE {settings.VIEW_USER} SET search_path=views,public"""
    )
    await connection.execute(
        """CREATE OR REPLACE VIEW views.product_updates_by_owner AS
      SELECT pu.updated_date,
        p.owners_tags owner_tag,
        ut.code update_type,
        count(*) update_count,
        count(DISTINCT pu.product_id) product_count
      FROM product_update pu
      JOIN product p ON p.id = pu.product_id
      JOIN update_type ut ON ut.id = pu.update_type_id
      GROUP BY pu.updated_date,
        p.owners_tags,
        ut.code"""
    )
    await connection.execute(f"""GRANT USAGE ON SCHEMA views TO {settings.VIEW_USER}""")
    await connection.execute(
        f"""GRANT SELECT ON views.product_updates_by_owner TO {settings.VIEW_USER}"""
    )
