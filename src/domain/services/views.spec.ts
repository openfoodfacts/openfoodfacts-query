import postgres from 'postgres';
import { randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { MessagesService } from './messages.service';
import { VIEW_PASSWORD, VIEW_USER } from '../../constants';

/*
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

    // Use viewer user
    const viewer = postgres({
      host: process.env.POSTGRES_HOST,
      database: process.env.POSTGRES_DB,
      user: VIEW_USER,
      password: VIEW_PASSWORD,
      port: parseInt(process.env.POSTGRES_PORT.split(':').pop()),
    });

    const results = await viewer`SELECT * from product_updates_by_owner`;

    const myResult = results.find((r) => r.owner_tag === owner1);
    expect(myResult.update_count).toBe(4);
    expect(myResult.product_count).toBe(2);
  });

  it('should update existing aggregate counts', async () => {
    // Create some products
    const code1 = randomCode();
    const action1 = randomCode();

    // Create an existing message
    const messages = new MessagesService();

    let idCount = 0;
    const nextId = () => `${Date.now()}-${idCount++}`;
    await messages.create([
      {
        id: nextId(),
        message: {
          code: code1,
          action: action1,
        },
      },
    ]);

    // Add another message
    await messages.create([
      {
        id: nextId(),
        message: {
          code: code1,
          action: action1,
        },
      },
    ]);

    // Use viewer user
    const viewer = postgres({
      host: process.env.POSTGRES_HOST,
      database: process.env.POSTGRES_DB,
      user: VIEW_USER,
      password: VIEW_PASSWORD,
      port: parseInt(process.env.POSTGRES_PORT.split(':').pop()),
    });

    const results = await viewer`SELECT * from product_updates_by_owner`;

    const myResult = results.find((r) => r.action === action1);
    expect(myResult.update_count).toBe(2);
    expect(myResult.product_count).toBe(1);
  });
});
*/