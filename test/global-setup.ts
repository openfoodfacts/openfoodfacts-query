import { PostgreSqlContainer } from '@testcontainers/postgresql';
import util from 'util';
import child_process from 'child_process';

const exec = util.promisify(child_process.exec);

export default async function () {
  // Use same image as docker-compose.yml to ensure we don't use unsupported features
  const container = await new PostgreSqlContainer(
    process.env.POSTGRES_IMAGE,
  ).start();
  process.env.POSTGRES_HOST = `${container.getHost()}:${container
    .getPort()
    .toString()}`;
  process.env.POSTGRES_DB = container.getDatabase();
  process.env.POSTGRES_USER = container.getUsername();
  process.env.POSTGRES_PASSWORD = container.getPassword();
  globalThis.__PGCONTAINER__ = container;

  // We don't use redis in the tests
  process.env.REDIS_URL = '';

  // Prevent tests from calling directly to MongoDB
  process.env.MONGO_URI = '';

  // Tried running migrations with the API but doesn't work because
  // of the way Jest mocks things. Even importing MikroORM is enough to break things.
  // https://github.com/mikro-orm/mikro-orm/discussions/3795
  await exec('npx mikro-orm migration:up');
}
