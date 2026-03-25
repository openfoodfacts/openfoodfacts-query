async def up(transaction):
    from query.config import config_settings

    # Create user for superset with adequate permissions and attributes
    # So that it can read data and access schema

    # remove superset role if exists
    # we have to fetch because we can't use "DROP OWNED" conditionally
    existing_user = await transaction.fetch(
        """SELECT 1 FROM pg_roles WHERE rolname = 'superset'"""
    )
    if existing_user:
        await transaction.execute(f"""
            DROP OWNED BY superset; \
            DROP ROLE IF EXISTS superset; \
            """)
    await transaction.execute(f"""
        CREATE ROLE superset LOGIN PASSWORD '{config_settings.POSTGRES_SUPERSET_PASSWORD}'; \
        GRANT pg_read_all_data TO superset; \
        GRANT USAGE ON  schema public, query TO superset; \
        ALTER ROLE superset SET search_path = public, query; \
        """)
