import { MikroORM, RequestContext } from '@mikro-orm/core';
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
  try {
    await RequestContext.createAsync(orm.em, async () => {
      await callback(app);
    });
  } finally {
    await orm.close();
  }
}
