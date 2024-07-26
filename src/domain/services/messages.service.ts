import { Injectable } from '@nestjs/common';
import sql from '../../db';

const nulRegex = /\\u0000/g;

@Injectable()
export class MessagesService {
  messageTime(message: any) {
    // First preference is to use timestamp in the message
    let time = new Date(parseInt(message.message?.timestamp) * 1000);
    // Otherwise derive from message id
    time = isNaN(time.getTime())
      ? new Date(parseInt(message.id?.split('-')[0]))
      : time;
    // Or use today's date/time if that doesn't work
    return isNaN(time.getTime()) ? new Date() : time;
  }

  async create(messages: any[]) {
    // Strip out any \u0000 characters as PostgresSQL can't cope with them
    const messageJson = JSON.stringify(messages);
    if (messageJson.includes('\\u0000')) {
      messages = JSON.parse(messageJson.replace(nulRegex, ''));
    }

    await sql`INSERT into product_update_event ${sql(
      messages.map((m) => ({
        id: m.id,
        updated_at: this.messageTime(m),
        code: m.message.code,
        message: m.message,
      })),
    )} ON CONFLICT DO NOTHING`;
  }
}
