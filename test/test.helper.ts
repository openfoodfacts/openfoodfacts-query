import { MikroORM, RequestContext } from '@mikro-orm/core';
import { logger } from '@mikro-orm/nestjs';
import { ConsoleLogger } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import { randomBytes } from 'crypto';

export function randomCode() {
  return 'TEST-' + randomBytes(20).toString('base64');
}

class TestLogger extends ConsoleLogger {
  errors = new Array<string>();
  expectedErrors = 0;
  constructor() {
    super();
    this.setLogLevels(['error']);
  }
  error(message: string, ...rest: any[]) {
    this.errors.push(message);
    if (this.errors.length > this.expectedErrors) {
      super.error(message, ...rest);
    }
  }
  assertExpectedErrors() {
    expect(this.errors).toHaveLength(this.expectedErrors);
  }
}

export async function createTestingModule(
  imports: any[],
  callback: { (app: TestingModule, logger: TestLogger): Promise<void> },
) {
  const testLogger = new TestLogger();
  const app = await Test.createTestingModule({
    imports: imports,
  }).compile();
  app.useLogger(testLogger);
  await app.init();

  const orm = app.get(MikroORM);
  try {
    await RequestContext.createAsync(orm.em, async () => {
      await callback(app, testLogger);
    });
    testLogger.assertExpectedErrors();
  } catch (e) {
    (e.errors ?? [e]).map((e) => logger.error(e.message, e.stack));
    throw e;
  } finally {
    await orm.close();
    await app.close();
  }
}
