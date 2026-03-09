async def up(transaction):
    from query.config import config_settings

    # Create user for superset with adequate permissions and attributes
    # So that it can read data and access schema
    await transaction.execute(
        f"""
        DROP OWNED BY superset; \
        DROP ROLE IF EXISTS superset; \
        CREATE ROLE superset LOGIN PASSWORD '{config_settings.POSTGRES_SUPERSET_PASSWORD}'; \
        GRANT pg_read_all_data TO superset; \
        GRANT USAGE ON  schema public, query TO superset; \
        ALTER ROLE superset SET search_path = public, query; \
        """
    )
