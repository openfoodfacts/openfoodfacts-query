from query.db import settings

async def create_schema(connection):
    await connection.execute("create schema if not exists views;")
    await connection.execute(
        f"""CREATE USER {settings.VIEW_USER} PASSWORD '{settings.VIEW_PASSWORD}'""")
    await connection.execute(
        f"""ALTER ROLE {settings.VIEW_USER} SET search_path=views,public"""
    )
    await connection.execute(f"""GRANT USAGE ON SCHEMA views TO {settings.VIEW_USER}""")
    