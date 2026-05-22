"""Creates a view only user to support direct database queries for dashboards, etc."""

from query.config import config_settings


async def create_schema(transaction):
    await transaction.execute("create schema if not exists views;")
    await transaction.execute(
        f"""CREATE USER {config_settings.VIEW_USER} PASSWORD '{config_settings.VIEW_PASSWORD}'"""
    )
    await transaction.execute(
        f"""ALTER ROLE {config_settings.VIEW_USER} SET search_path=views,public"""
    )
    await transaction.execute(
        f"""GRANT USAGE ON SCHEMA views TO {config_settings.VIEW_USER}"""
    )
