import { createClient } from 'redis';
import { GenericContainer } from 'testcontainers';
import { createTestingModule, randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { DomainModule } from '../domain.module';
import { ImportService } from './import.service';
import { SettingsService } from './settings.service';
import { RedisListener } from './redis.listener';
import { setTimeout } from 'timers/promises';

// Allow a little time for the testcontainer to start
jest.setTimeout(300000);

describe('receiveMessages', () => {
  it('should call importwithfilter when a message is received', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: Redis is running
      const redis = await new GenericContainer('redis')
        .withExposedPorts(6379)
        .start();
      const redisUrl = `redis://localhost:${redis.getMappedPort(6379)}`;
      const settings = app.get(SettingsService);
      jest.spyOn(settings, 'getRedisUrl').mockImplementation(() => redisUrl);

      // And lastmessageid is zero
      await settings.setLastMessageId('0');
      const importService = app.get(ImportService);
      const importSpy = jest
        .spyOn(importService, 'importWithFilter')
        .mockImplementation();

      const redisListener = app.get(RedisListener);
      await redisListener.startRedisConsumer();

      const client = createClient({ url: redisUrl });
      await client.connect();
      try {
        const code1 = randomCode();
        const code2 = randomCode();

        // When: A message is sent
        const messageId = await client.xAdd('product_updates_off', '*', {
          code: code1,
        });

        // Wait for message to be delivered
        await setTimeout(100);

        // Then the import is called
        expect(importSpy).toHaveBeenCalledTimes(1);
        expect(await settings.getLastMessageId()).toBe(messageId);

        // If a new message is added
        importSpy.mockClear();
        await client.xAdd('product_updates_off', '*', {
          code: code2,
        });

        // Wait for message to be delivered
        await setTimeout(100);

        // Then import is called again but only with the new code
        expect(importSpy).toHaveBeenCalledTimes(1);
        const codes = importSpy.mock.calls[0][0].code.$in;
        expect(codes).toHaveLength(1);
        expect(codes[0]).toBe(code2);

        // Update events are created
        const events =
          await sql`SELECT * FROM product_update_event WHERE message->>'code' = ${code1}`;

        expect(events).toHaveLength(1);
        expect(events[0].id).toBe(messageId);
      } finally {
        await client.quit();
        await redisListener.stopRedisConsumer();
        await redis.stop();
      }
    });
  });
});

describe('processMessages', () => {
  it('should not call importwithfilter for messages that contain the initial_import diff', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      const importSpy = jest
        .spyOn(importService, 'importWithFilter')
        .mockImplementation();

      const code1 = randomCode();
      const code2 = randomCode();
      let idCount = 0;
      const nextId = () => `${Date.now()}-${idCount++}`;
      const messages = [
        {
          id: nextId(),
          message: {
            code: code1,
          },
        },
        {
          id: nextId(),
          message: {
            code: code2,
            // Note JSON properties in Redis come in as strings
            diffs: JSON.stringify({
              initial_import: 1,
            }),
          },
        },
      ];

      const redisListener = app.get(RedisListener);
      await redisListener.processMessages(messages);
      // Then the import is called only once for code1
      const codes = importSpy.mock.calls[0][0].code.$in;
      expect(codes).toHaveLength(1);
      expect(codes[0]).toBe(code1);

      // Update events are created for all codes
      const events =
        await sql`SELECT * FROM product_update_event WHERE message->>'code' IN ${sql(
          [code1, code2],
        )}`;

      expect(events).toHaveLength(2);
    });
  });

  it('should not call importwithfilter at all if all messages contain the initial_import diff', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      const importSpy = jest
        .spyOn(importService, 'importWithFilter')
        .mockImplementation();

      const code1 = randomCode();
      const code2 = randomCode();
      let idCount = 0;
      const nextId = () => `${Date.now()}-${idCount++}`;
      const messages = [
        {
          id: nextId(),
          message: {
            code: code1,
            // Note JSON properties in Redis come in as strings
            diffs: JSON.stringify({
              initial_import: 1,
            }),
          },
        },
        {
          id: nextId(),
          message: {
            code: code2,
            // Note JSON properties in Redis come in as strings
            diffs: JSON.stringify({
              initial_import: 1,
            }),
          },
        },
      ];

      const redisListener = app.get(RedisListener);
      await redisListener.processMessages(messages);
      // Then the import is not called at all
      expect(importSpy).toHaveBeenCalledTimes(0);

      // Update events are created for all codes
      const events =
        await sql`SELECT * FROM product_update_event WHERE code IN ${sql([
          code1,
          code2,
        ])}`;

      expect(events).toHaveLength(2);
    });
  });
});
