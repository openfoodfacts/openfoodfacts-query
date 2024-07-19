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
    const date = importService.messageTime({ timestamp: time });
    expect(date.getTime()).toBe(time * 1000);
  });
});

describe('create', () => {
  it('should ignore duplicate events', async () => {
    const code1 = randomCode();
    const messages = new MessagesService();
    await messages.create([
      {
        id: '1-0',
        message: {
          code: code1,
        },
      },
      {
        id: '1-0',
        message: {
          code: code1,
        },
      },
    ]);

    const result =
      await sql`SELECT * FROM product_update_event WHERE code = ${code1}`;
    expect(result).toHaveLength(1);
  });
});
