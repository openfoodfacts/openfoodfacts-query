import { randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { MessagesService } from './messages.service';

describe('messageTime', () => {
  it('should return a date from a message id', () => {
    const importService = new MessagesService();
    const time = Date.now() - 1000;
    const date = importService.messageTime({ id: `${time}-0` });
    expect(date.getTime()).toBe(time);
  });
  it('should return the current date for an invalid message id', () => {
    const importService = new MessagesService();
    const now = Date.now();
    const date = importService.messageTime({ id: 'invalid' });
    expect(date.getTime()).toBeGreaterThanOrEqual(now);
  });
  it('should cope with a null id', async () => {
    const importService = new MessagesService();
    const now = Date.now();
    const date = importService.messageTime({ id: null });
    expect(date.getTime()).toBeGreaterThanOrEqual(now);
  });
  it('should cope with no id', async () => {
    const importService = new MessagesService();
    const now = Date.now();
    const date = importService.messageTime({});
    expect(date.getTime()).toBeGreaterThanOrEqual(now);
  });
  it('should use timestamp if provided', async () => {
    const importService = new MessagesService();
    const time = Math.trunc((Date.now() - 1000) / 1000);
    const date = importService.messageTime({
      id: '100-0',
      message: { timestamp: time },
    });
    expect(date.getTime()).toBe(time * 1000);
  });
});

let idCount = 0;

describe('create', () => {
  it('should ignore duplicate events', async () => {
    const code1 = randomCode();
    const messages = new MessagesService();
    const messageId = `${Date.now()}-${idCount++}`;

    await messages.create([
      {
        id: messageId,
        message: {
          code: code1,
        },
      },
      {
        id: messageId,
        message: {
          code: code1,
        },
      },
    ]);

    const result =
      await sql`SELECT * FROM product_update_event WHERE code = ${code1}`;
    expect(result).toHaveLength(1);
  });

  it('should cope with null characters', async () => {
    const code1 = randomCode();
    const messages = new MessagesService();
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
      await sql`SELECT * FROM product_update_event WHERE code = ${code1}`;
    expect(result).toHaveLength(1);
    expect(result[0].message.comment).toBe('test  test2  end');
  });
});
