import { PostgreSqlContainer } from '@testcontainers/postgresql';

export default async function () {
  const container = await new PostgreSqlContainer().start();
  process.env.POSTGRES_HOST = container.getHost();
  process.env.POSTGRES_PORT = container.getPort().toString();
  process.env.POSTGRES_DB = container.getDatabase();
  process.env.POSTGRES_USER = container.getUsername();
  process.env.POSTGRES_PASSWORD = container.getPassword();

  // Tried running migrations here but get this error: https://github.com/mikro-orm/mikro-orm/discussions/3795
  // Removing jest.mock calls didn't help

  globalThis.__PGCONTAINER__ = container;
}
