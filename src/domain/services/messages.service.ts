import { Injectable, Logger } from '@nestjs/common';
import sql from '../../db';
import { ImportService } from './import.service';
import { ProductSource } from '../enums/product-source';

const nulRegex = /\\u0000/g;

@Injectable()
export class MessagesService {
  private logger = new Logger(MessagesService.name);

  constructor(private readonly importService: ImportService) {}

  static messageTime(message: any) {
    // First preference is to use timestamp in the message
    let time = new Date(parseInt(message.message?.timestamp) * 1000);
    // Otherwise derive from message id
    time = isNaN(time.getTime())
      ? new Date(parseInt(message.id?.split('-')[0]))
      : time;
    // Or use today's date/time if that doesn't work
    return isNaN(time.getTime()) ? new Date() : time;
  }

  async create(messages: any[], initialImport = false) {
    // Strip out any \u0000 characters as PostgresSQL can't cope with them
    const messageJson = JSON.stringify(messages);
    if (messageJson.includes('\\u0000')) {
      messages = JSON.parse(messageJson.replace(nulRegex, ''));
    }

    const receivedAt = new Date();
    const insertResult = await sql`INSERT into product_update_event ${sql(
      messages.map((m) => ({
        message_id: m.id,
        received_at: receivedAt,
        updated_at: MessagesService.messageTime(m),
        message: m.message,
      })),
    )} RETURNING (id)`;

    const messageIds = insertResult.map((m) => m.id);

    await sql`insert into contributor (code)
      select distinct message->>'user_id'
      from product_update_event 
      where id in ${sql(messageIds)}
      and not exists (select * from contributor where code = message->>'user_id')
      on conflict (code)
      do nothing`;

    await sql`insert into update_type (code)
      select distinct message->>'action'
      from product_update_event 
      where id in ${sql(messageIds)}
      and not exists (select * from update_type where code = message->>'action')
      on conflict (code)
      do nothing`;

    if (!initialImport) {
      const productCodes = [
        ...new Set(
          messages
            // At the moment we only import food products. This can be removed when we import all flavours
            .filter((m) => m.message.product_type === 'food')
            .map((m) => m.message.code),
        ),
      ];
      if (productCodes.length) {
        const filter = { code: { $in: productCodes } };
        await this.importService.importWithFilter(filter, ProductSource.EVENT);
      }
    }

    // Update counts on product_update after products have been imported
    // Note coalesce on rev is only needed for transition if an older version of PO is deployed
    await sql`INSERT INTO product_update (
        product_id,
        revision,
        updated_date,
        update_type_id,
        contributor_id,
        event_id)
      SELECT 
      	p.id,
        coalesce((pe.message->>'rev')::int, p.revision),
        date(pe.updated_at at time zone 'UTC') updated_day,
        update_type.id,
        contributor.id,
        pe.id
      FROM product_update_event pe
        JOIN product p on p.code = pe.message->>'code'
        join contributor on contributor.code = pe.message->>'user_id'
        join update_type on update_type.code = pe.message->>'action'
      where pe.id in ${sql(messageIds)}
      on conflict (product_id,revision) DO NOTHING`;

    this.logger.log(`Received ${messages.length} events`);
  }
}
