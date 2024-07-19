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
});
