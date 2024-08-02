import postgres from 'postgres';
import { createTestingModule, randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { MessagesService } from './messages.service';
import { VIEW_PASSWORD, VIEW_USER } from '../../constants';
import { DomainModule } from '../domain.module';

describe('product_update', () => {
  it('should aggregate events by count and distinct products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const messages = app.get(MessagesService);
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
      let idCount = 0;
      const nextId = () => `${Date.now()}-${idCount++}`;
      await messages.create([
        {
          id: nextId(),
          message: {
            code: code1,
            action: 'updated',
            user_id: 'user1',
            diffs: { initial_import: 1 },
          },
        },
        {
          id: nextId(),
          message: {
            code: code1,
            action: 'updated',
            user_id: 'user1',
            diffs: { initial_import: 1 },
          },
        },
        {
          id: nextId(),
          message: {
            code: code1,
            action: 'updated',
            user_id: 'user1',
            diffs: { initial_import: 1 },
          },
        },
        {
          id: nextId(),
          message: {
            code: code2,
            action: 'updated',
            user_id: 'user1',
            diffs: { initial_import: 1 },
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

      const results = await viewer`SELECT 
          owners_tags owner_tag,
          sum(update_count) update_count,
          count(DISTINCT product_id) product_count 
        from product_update pu
        join product p on p.id= pu.product_id
        group by owners_tags`;

      const myResult = results.find((r) => r.owner_tag === owner1);
      expect(myResult.update_count).toBe('4');
      expect(myResult.product_count).toBe('2');
    });
  });

  it('should update existing aggregate counts', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const messages = app.get(MessagesService);
      // Create some products
      const code1 = randomCode();
      const action1 = randomCode();

      await sql`INSERT INTO product ${sql([
        {
          code: code1,
        },
      ])}`;

      // Create an existing message
      let idCount = 0;
      const nextId = () => `${Date.now()}-${idCount++}`;
      await messages.create([
        {
          id: nextId(),
          message: {
            code: code1,
            action: action1,
            user_id: 'user1',
            diffs: { initial_import: 1 },
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
            user_id: 'user1',
            diffs: { initial_import: 1 },
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

      const results = await viewer`SELECT 
          ut.code update_type,
          sum(update_count) update_count,
          count(DISTINCT product_id) product_count
        from product_update pu
        join update_type ut on ut.id = pu.update_type_id
        group by ut.code`;

      const myResult = results.find((r) => r.update_type === action1);
      expect(myResult.update_count).toBe('2');
      expect(myResult.product_count).toBe('1');
    });
  });
});
