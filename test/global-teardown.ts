export default async function () {
  await globalThis.__PGCONTAINER__.stop();
}
