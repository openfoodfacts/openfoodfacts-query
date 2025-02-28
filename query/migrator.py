import logging
import os
from asyncpg import Connection
from query.db import settings
MIGRATIONS_TABLE = 'mikro_orm_migrations'
MIGRATIONS_FOLDER = 'migrations'

logger = logging.getLogger(__name__)

async def ensure_migration_table(connection: Connection):
    await connection.execute(f'create schema if not exists {settings.SCHEMA};')
    await connection.execute(f"SET search_path={settings.SCHEMA},public")
    await connection.execute(
        f"ALTER ROLE {settings.POSTGRES_USER} SET search_path={settings.SCHEMA},public",
    )

    # Use the Mikro-ORM table to keep database compatibility
    await connection.execute(f'''CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
        id serial4 PRIMARY KEY, 
        name varchar(255) NULL, 
        executed_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL
    )''')
    
async def migrate_database(connection: Connection):
    await ensure_migration_table(connection)
    rows = await connection.fetch(f'SELECT * FROM {MIGRATIONS_TABLE}')
    existing_migrations = [r['name'] for r in rows]
    for fname in sorted(os.listdir(MIGRATIONS_FOLDER)):
        if fname.endswith('.py') and not fname.startswith('__'):
            migration_name = fname.split('.')[0]
            if migration_name not in existing_migrations:
                logger.info(f'Applying {fname}')
                module_name = '.'.join(fname.split('.')[:-1])
                m = __import__(f'{MIGRATIONS_FOLDER}.{module_name}')
                module = getattr(m, module_name)
                async with connection.transaction():
                    await module.up(connection)
                    await connection.execute(f'INSERT INTO {MIGRATIONS_TABLE} (name) VALUES ($1)', migration_name)
