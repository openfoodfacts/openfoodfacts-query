import { randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { MessagesService } from './messages.service';

describe('product_updates_view', () => {
  it('should aggregate events by count and distinct products', async () => {
    // Create some products
    const code1 = randomCode();
    const code2 = randomCode();
    const owner1 = randomCode();

    await sql`INSERT INTO product ${sql([
      {
        code: code1,
        owners_tags: owner1,
      },
      {
        code: code2,
        owners_tags: owner1,
      },
    ])}`;

    // Create some messages
    const messages = new MessagesService();

    let idCount = 0;
    const nextId = () => `${Date.now()}-${idCount++}`;
    await messages.create([
      {
        id: nextId(),
        message: {
          code: code1,
        },
      },
      {
        id: nextId(),
        message: {
          code: code1,
        },
      },
      {
        id: nextId(),
        message: {
          code: code1,
        },
      },
      {
        id: nextId(),
        message: {
          code: code2,
        },
      },
    ]);

    const results = await sql`SELECT 
        DATE_TRUNC('day', pe.updated_at) updated_day,
        p.owners_tags,
        count(*) update_count,
        count(DISTINCT pe.code) product_count
    FROM product_update_event pe
        LEFT JOIN product p on p.code = pe.code
    GROUP BY DATE_TRUNC('day', pe.updated_at),
        p.owners_tags`;

    const myResult = results.find((r) => r.owners_tags === owner1);
    expect(myResult.update_count).toBe('4');
    expect(myResult.product_count).toBe('2');
  });
});
