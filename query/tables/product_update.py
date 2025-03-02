async def create_table(connection):
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
