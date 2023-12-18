import { MikroORM } from '@mikro-orm/core';
import { PostgreSqlContainer } from '@testcontainers/postgresql';

export default async function () {
  const container = await new PostgreSqlContainer().start();
  process.env.POSTGRES_HOST = container.getHost();
  process.env.POSTGRES_PORT = container.getPort().toString();
  process.env.POSTGRES_DB = container.getDatabase();
  process.env.POSTGRES_USER = container.getUsername();
  process.env.POSTGRES_PASSWORD = container.getPassword();

  // Don't import the MikroORM config at start as need the env vars to be set
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const config = require('../src/mikro-orm.config').default;
  const orm = await MikroORM.init({ ...config, logger: () => null });
  await orm.getMigrator().up();
  await orm.close();

  globalThis.__PGCONTAINER__ = container;
}
