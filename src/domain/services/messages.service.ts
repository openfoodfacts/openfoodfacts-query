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

    const results = await sql`insert into contributor (code)
      select distinct message->>'user_id'
      from product_update_event 
      where id in ${sql(messageIds)}
      on conflict (code)
      do nothing`;
    /*
    const [minTime, maxTime] = messagesForInsert.reduce(
      ([prevMin, prevMax], m) => [
        Math.min(prevMin, m.updated_at.getTime()),
        Math.max(prevMax, m.updated_at.getTime()),
      ],
      [Infinity, -Infinity],
    );

    const minDate = new Date(minTime).toISOString().substring(0, 10);
    const maxDate = new Date(maxTime + 86400000).toISOString().substring(0, 10);

    // TODO: When we upgrade to PostgreSQL 15 we can us a unique constraint to cover the nullable columns
    // so won't need to expressions in the on conflict clause
    await sql`INSERT INTO product_updates_by_owner
      SELECT 
        date(pe.updated_at at time zone 'UTC') updated_day,
        p.owners_tags owner_tag,
        pe.action,
        count(*) update_count,
        count(DISTINCT pe.code) product_count
      FROM product_update_event pe
        LEFT JOIN product p on p.code = pe.code
      WHERE pe.updated_at >= ${minDate} AND pe.updated_at < ${maxDate}
      GROUP BY date(pe.updated_at at time zone 'UTC'),
        p.owners_tags,
        pe.action
      on conflict (updated_date, coalesce(owner_tag, ''), coalesce(action, ''))
       do update set 
      	update_count = EXCLUDED.update_count,
      	product_count = EXCLUDED.product_count`;
    */
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
    await this.settings.setLastMessageId(messages[messages.length - 1].id);
  }
}
