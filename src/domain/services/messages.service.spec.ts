import { createTestingModule, randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { DomainModule } from '../domain.module';
import { MessagesService } from './messages.service';

describe('messageTime', () => {
  it('should return a date from a message id', () => {
    const time = Date.now() - 1000;
    const date = MessagesService.messageTime({ id: `${time}-0` });
    expect(date.getTime()).toBe(time);
  });
  it('should return the current date for an invalid message id', () => {
    const now = Date.now();
    const date = MessagesService.messageTime({ id: 'invalid' });
    expect(date.getTime()).toBeGreaterThanOrEqual(now);
  });
  it('should cope with a null id', async () => {
    const now = Date.now();
    const date = MessagesService.messageTime({ id: null });
    expect(date.getTime()).toBeGreaterThanOrEqual(now);
  });
  it('should cope with no id', async () => {
    const now = Date.now();
    const date = MessagesService.messageTime({});
    expect(date.getTime()).toBeGreaterThanOrEqual(now);
  });
  it('should use timestamp if provided', async () => {
    const time = Math.trunc((Date.now() - 1000) / 1000);
    const date = MessagesService.messageTime({
      id: '100-0',
      message: { timestamp: time },
    });
    expect(date.getTime()).toBe(time * 1000);
  });
});

let idCount = 0;

describe('create', () => {
  it('should ignore duplicate events', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const messages = app.get(MessagesService);
      const code1 = randomCode();
      const messageId = `${Date.now()}-${idCount++}`;

      await messages.create([
        {
          id: messageId,
          message: {
            code: code1,
            action: 'created',
          },
        },
        {
          id: messageId,
          message: {
            code: code1,
            action: 'created',
          },
        },
      ]);

      const result =
        await sql`SELECT * FROM product_update_event WHERE message->>'code' = ${code1}`;
      expect(result).toHaveLength(1);
      expect(result[0].message.action).toBe('created');
    });
  });

  it('should cope with null characters', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const messages = app.get(MessagesService);
      const code1 = randomCode();
      await messages.create([
        {
          id: `${Date.now()}-${idCount++}`,
          message: {
            code: code1,
            comment: 'test \u0000 test2 \u0000 end',
          },
        },
      ]);

      const result =
        await sql`SELECT * FROM product_update_event WHERE message->>'code' = ${code1}`;
      expect(result).toHaveLength(1);
      expect(result[0].message.comment).toBe('test  test2  end');
    });
  });

  it('should create contributors', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const messages = app.get(MessagesService);
      const code1 = randomCode();
      const user1 = randomCode();
      const user2 = randomCode();

      // Given and existing contributor record
      sql`INSERT INTO contributor (code) VALUES(${user1})`;

      // When events are imported
      await messages.create([
        {
          id: `${Date.now()}-${idCount++}`,
          message: {
            code: code1,
            user_id: user1,
            action: 'created',
          },
        },
        {
          id: `${Date.now()}-${idCount++}`,
          message: {
            code: code1,
            user_id: user2,
            action: 'created',
          },
        },
      ]);

      const result = await sql`SELECT * FROM contributor WHERE code = ${user2}`;
      expect(result).toHaveLength(1);
    });
  });
});
