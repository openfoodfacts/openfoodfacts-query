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
  await app.init();

  const orm = app.get(MikroORM);
  try {
    await RequestContext.createAsync(orm.em, async () => {
      await callback(app);
    });
  } catch (e) {
    (e.errors ?? [e]).map((e) => logger.error(e.message, e.stack));
    throw e;
  } finally {
    await orm.close();
    await app.close();
  }
}
