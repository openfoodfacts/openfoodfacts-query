import { Injectable } from '@nestjs/common';
import sql from '../../db';

@Injectable()
export class MessagesService {
  messageTime(message: any) {
    const time = new Date(parseInt(message.id?.split('-')[0]));
    return isNaN(time.getTime()) ? new Date() : time;
  }

  async create(messages: any[]) {
    await sql`INSERT into product_update_event ${sql(
      messages.map((m) => ({
        id: m.id,
        updated_at: this.messageTime(m),
        code: m.message.code,
        message: m.message,
      })),
    )}`;
  }
}
