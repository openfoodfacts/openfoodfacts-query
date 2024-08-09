import { createClient } from 'redis';
import { GenericContainer } from 'testcontainers';
import { createTestingModule, randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { DomainModule } from '../domain.module';
import { ImportService } from './import.service';
import { SettingsService } from './settings.service';
import { RedisListener } from './redis.listener';
import { setTimeout } from 'timers/promises';
import { MessagesService } from './messages.service';

// Allow a little time for the testcontainer to start
jest.setTimeout(300000);

describe('receiveMessages', () => {
  it('should call importWithFilter when a message is received', async () => {
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
          rev: '1',
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
        expect(events[0].message_id).toBe(messageId);
      } finally {
        await client.quit();
        await redisListener.stopRedisConsumer();
        await redis.stop();
      }
    });
  });
});

describe('processMessages', () => {
  it('should convert json properties to objects', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const messagesService = app.get(MessagesService);
      const createSpy = jest
        .spyOn(messagesService, 'create')
        .mockImplementation();

      const messages = [
        {
          id: `0-0`,
          message: {
            code: 'test',
            diffs: `{"action":"update"}`,
          },
        },
      ];

      const redisListener = app.get(RedisListener);
      await redisListener.processMessages(messages);

      // Then create is called with a real object
      const diffs = createSpy.mock.calls[0][0][0].message.diffs;
      expect(diffs.action).toBe('update');
    });
  });
});
