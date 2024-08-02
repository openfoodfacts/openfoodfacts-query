import { Injectable, Logger } from '@nestjs/common';
import sql from '../../db';
import { ImportService } from './import.service';
import { SettingsService } from './settings.service';
import { ProductSource } from '../enums/product-source';

const nulRegex = /\\u0000/g;

@Injectable()
export class MessagesService {
  private logger = new Logger(MessagesService.name);

  constructor(
    private readonly importService: ImportService,
    private readonly settings: SettingsService,
  ) {}

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

  async create(messages: any[]) {
    // Strip out any \u0000 characters as PostgresSQL can't cope with them
    const messageJson = JSON.stringify(messages);
    if (messageJson.includes('\\u0000')) {
      messages = JSON.parse(messageJson.replace(nulRegex, ''));
    }

    await sql`INSERT into product_update_event ${sql(
      messages.map((m) => ({
        id: m.id,
        updated_at: MessagesService.messageTime(m),
        message: m.message,
      })),
    )} ON CONFLICT DO NOTHING`;

    const messageIds = messages.map((m) => m.id);

    await sql`insert into contributor (code)
      select distinct message->>'user_id'
      from product_update_event 
      where id in ${sql(messageIds)}
      on conflict (code)
      do nothing`;

    await sql`insert into action (code)
      select distinct message->>'action'
      from product_update_event 
      where id in ${sql(messageIds)}
      on conflict (code)
      do nothing`;

    const productCodes = [
      ...new Set(
        messages
          .filter((m) => !m.message.diffs?.initial_import) // Don't trigger product updates on initial import
          .map((m) => m.message.code),
      ),
    ];
    this.logger.log(
      `Received ${messages.length} events with ${productCodes.length} products to import`,
    );
    if (productCodes.length) {
      const filter = { code: { $in: productCodes } };
      await this.importService.importWithFilter(filter, ProductSource.EVENT);
    }

    // Update counts on product_update after products have been imported
    await sql`INSERT INTO product_update
      SELECT 
      	p.id,
        date(pe.updated_at at time zone 'UTC') updated_day,
        action.id,
        contributor.id,
        count(*) update_count
      FROM product_update_event pe
        JOIN product p on p.code = pe.message->>'code'
        join contributor on contributor.code = pe.message->>'user_id'
        join action on action.code = pe.message->>'action'
      where pe.id in ${sql(messageIds)}
      GROUP BY p.id,
        date(pe.updated_at at time zone 'UTC'),
        action.id,
        contributor.id
       on conflict (updated_date,product_id,action,contributor_id)
       do update set 
      	update_count = product_update.update_count + EXCLUDED.update_count`;

    await this.settings.setLastMessageId(messages[messages.length - 1].id);
  }
}
