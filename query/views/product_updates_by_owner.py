from query.db import config_settings

async def create_view(connection):
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
    await connection.execute(
        f"""GRANT SELECT ON views.product_updates_by_owner TO {config_settings.VIEW_USER}"""
    )
