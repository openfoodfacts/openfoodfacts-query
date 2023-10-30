import { DomainModule } from '../domain.module';
import { ImportService } from './import.service';
import { EntityManager } from '@mikro-orm/core';
import { Product } from '../entities/product';
import { ProductIngredientsTag } from '../entities/product-tags';
import { createTestingModule, randomCode } from '../../../test/test.helper';

let index = 0;
const productIdNew = randomCode();
const productIdExisting = randomCode();
const products = [
  {
    // This one will be new
    code: productIdNew,
    last_modified_t: 1692032161,
    ingredients_tags: ['test'],
  },
  {
    // This one will already exist
    code: productIdExisting,
    last_modified_t: 1692032161,
    ingredients_tags: ['new_ingredient', 'old_ingredient'],
  },
];

jest.mock('mongodb', () => {
  return {
    MongoClient: jest.fn(() => ({
      connect: jest.fn(),
      db: () => ({
        collection: () => ({
          find: () => ({
            next: async () => {
              return index++ <= products.length ? products[index - 1] : null;
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
  it('should import a new product update existing products and not delete existing products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      importService.deleteAllProducts = jest.fn();

      // GIVEN: Two existing products, one of which is in Mongo plus one new one in Mongo
      const em = app.get(EntityManager);
      const productExisting = em.create(Product, { code: productIdExisting });
      em.create(ProductIngredientsTag, {
        product: productExisting,
        value: 'old_ingredient',
      });

      const productIdUnchanged = randomCode();
      const productUnchanged = em.create(Product, { code: productIdUnchanged });
      em.create(ProductIngredientsTag, {
        product: productUnchanged,
        value: 'unchanged_ingredient',
      });

      // WHEN:Doing a full import from MongoDB
      await importService.importFromMongo();

      // THEN: New product is addeded, updated product is updated and other product is unchanged
      expect(importService.deleteAllProducts).not.toHaveBeenCalled();
      const productNew = await em.findOne(Product, { code: productIdNew });
      expect(productNew).toBeTruthy();
      const ingredientsNew = await em.find(ProductIngredientsTag, {
        product: productNew,
      });
      expect(ingredientsNew).toHaveLength(1);
      expect(ingredientsNew[0].value).toBe('test');

      const ingredientsExisting = await em.find(ProductIngredientsTag, {
        product: productExisting,
      });
      expect(ingredientsExisting).toHaveLength(2);
      expect(
        ingredientsExisting.find((i) => i.value === 'old_ingredient'),
      ).toBeTruthy();
      expect(
        ingredientsExisting.find((i) => i.value === 'new_ingredient'),
      ).toBeTruthy();

      const ingredientsUnchanged = await em.find(ProductIngredientsTag, {
        product: productUnchanged,
      });
      expect(ingredientsUnchanged).toHaveLength(1);
      expect(ingredientsUnchanged[0].value).toBe('unchanged_ingredient');
    });
  });
});
