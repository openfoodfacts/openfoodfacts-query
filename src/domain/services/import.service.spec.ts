import { DomainModule } from '../domain.module';
import { ImportService } from './import.service';
import { EntityManager } from '@mikro-orm/core';
import { Product } from '../entities/product';
import { ProductIngredientsTag } from '../entities/product-tags';
import { createTestingModule, randomCode } from '../../../test/test.helper';

let index = 0;
const productId = randomCode();
jest.mock('mongodb', () => {
  return {
    MongoClient: jest.fn(() => ({
      connect: jest.fn(),
      db: () => ({
        collection: () => ({
          find: () => ({
            next: async () => {
              return index++ < 1
                ? {
                    code: productId,
                    last_modified_t: 1692032161,
                    ingredients_tags: ['test'],
                  }
                : null;
            },
            close: jest.fn(),
          }),
        }),
      }),
      close: jest.fn(),
    })),
  };
});

describe('importFromMongo', () => {
  it('should import a new product', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      importService.deleteAllProducts = jest.fn();
      await importService.importFromMongo();

      expect(importService.deleteAllProducts).toHaveBeenCalled();
      const em = app.get(EntityManager);
      const product = await em.findOne(Product, { code: productId });
      expect(product).toBeTruthy();
      const ingredients = await em.findOne(ProductIngredientsTag, {
        product: product,
      });
      expect(ingredients).toBeTruthy();
    });
  });
});
