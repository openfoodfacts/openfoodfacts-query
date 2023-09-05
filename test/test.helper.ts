import { MikroORM, RequestContext } from '@mikro-orm/core';
import { logger } from '@mikro-orm/nestjs';
import { Test, TestingModule } from '@nestjs/testing';
import { randomBytes } from 'crypto';

export function randomCode() {
  return 'TEST-' + randomBytes(20).toString('base64');
}

export async function createTestingModule(
  imports: any[],
  callback: { (app: TestingModule): Promise<void> },
) {
  const app = await Test.createTestingModule({
    imports: imports,
  }).compile();

  const orm = app.get(MikroORM);

  // Code here took a lot of attempts to get right
  // If just do migrations without constraints then they can interfere with each other
  // Tried doing migraitons in the global-setup script but that doesn't work due to a Jest issue
  const connection = orm.em.getConnection();
  try {
    await connection.execute(
      `CREATE TABLE if not exists lock_table(id int4 NOT NULL)`,
    );
  } catch (e) {}
  await connection.execute('BEGIN');
  await connection.execute(`LOCK TABLE lock_table`);
  await orm.getMigrator().up({ transaction: orm.em.getTransactionContext() });
  await connection.execute(`COMMIT`);

  try {
    await RequestContext.createAsync(orm.em, async () => {
      await callback(app);
    });
  } catch (e) {
    (e.errors ?? [e]).map((e) => logger.error(e.message, e.stack));
    throw e;
  } finally {
    await orm.close();
  }
}
