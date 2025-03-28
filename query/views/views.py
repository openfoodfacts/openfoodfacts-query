from query.config import config_settings


async def create_schema(connection):
    await connection.execute("create schema if not exists views;")
    await connection.execute(
        f"""CREATE USER {config_settings.VIEW_USER} PASSWORD '{config_settings.VIEW_PASSWORD}'"""
    )
    await connection.execute(
        f"""ALTER ROLE {config_settings.VIEW_USER} SET search_path=views,public"""
    )
    await connection.execute(
        f"""GRANT USAGE ON SCHEMA views TO {config_settings.VIEW_USER}"""
    )
