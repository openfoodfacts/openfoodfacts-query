import sql from '../src/db';

export default async function () {
  await sql.end();
  await globalThis.__PGCONTAINER__.stop();
}
