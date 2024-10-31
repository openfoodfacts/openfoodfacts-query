import { DomainModule } from '../domain.module';
import { ImportService } from './import.service';
import { EntityManager } from '@mikro-orm/postgresql';
import { Product } from '../entities/product';
import { ProductIngredientsTag } from '../entities/product-tags';
import { createTestingModule, randomCode } from '../../../test/test.helper';
import { TagService } from './tag.service';
import { LoadedTag } from '../entities/loaded-tag';
import { ProductTagMap } from '../entities/product-tag-map';
import { ProductSource } from '../enums/product-source';
import { SettingsService } from './settings.service';
import { ProductIngredient } from '../entities/product-ingredient';
import sql from '../../db';

const lastUpdated = 1692032161;

function testProducts() {
  const productIdNew = randomCode();
  const productIdExisting = randomCode();
  const products = [
    {
      // This one will be new
      code: productIdNew,
      last_updated_t: lastUpdated,
      ingredients_tags: ['test'],
      rev: 1,
    },
    {
      // This one will already exist
      code: productIdExisting,
      last_updated_t: lastUpdated,
      ingredients_tags: ['new_ingredient', 'old_ingredient'],
    },
  ];
  return { products, productIdExisting, productIdNew };
}

const findCalls = [];

jest.mock('mongodb', () => {
  return {
    MongoClient: jest.fn(() => ({
      connect: jest.fn(),
      db: () => {
        return {
          collection: (collectionName) => {
            let index = 0;
            const productList =
              collectionName === 'products' ? mockedProducts : [];
            return {
              find: (...args: any) => {
                findCalls.push(args);
                return {
                  next: async () => {
                    return index++ <= productList.length
                      ? productList[index - 1]
                      : null;
                  },
                  close: jest.fn(),
                };
              },
            };
          },
        };
      },
      close: jest.fn(),
    })),
  };
});

let mockedProducts = [];
function mockMongoDB(productList) {
  mockedProducts = productList;
}

// Import tests can sometimes take a little time in GitHub
jest.setTimeout(300000);

describe('importFromMongo', () => {
  it('should import a new product update existing products and delete missing products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // To see Mikro-ORM log output you need to make sure NestJS isn't using it's TestLogger
      // And also uncomment the debug setting in mikro-orm.config.ts
      // app.useLogger(new Logger());

      const importService = app.get(ImportService);
      // Mock the process id so it doesn't delete records from other tests
      let currentProcessId = 99999999999999999n;
      importService.getProcessId = jest
        .fn()
        .mockImplementation(() => ++currentProcessId);

      // GIVEN: Two existing products, one of which is in Mongo plus one new one in Mongo
      const em = app.get(EntityManager);
      const { products, productIdExisting, productIdNew } = testProducts();
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
      // Delete a tag to prove it is re-created
      await em.nativeDelete(LoadedTag, { id: 'teams_tags' });
      await em.flush();

      // WHEN:Doing a full import from MongoDB
      mockMongoDB(products);
      const start = Date.now();

      await importService.importFromMongo();

      // THEN: New product is added, updated product is updated and other product is unchanged
      const productNew = await em.findOne(Product, { code: productIdNew });
      expect(productNew).toBeTruthy();
      expect(productNew.processId).toBe(currentProcessId.toString());
      expect(productNew.source).toBe(ProductSource.FULL_LOAD);
      expect(productNew.lastProcessed.getTime()).toBeGreaterThanOrEqual(start);
      const ingredientsNew = await em.find(ProductIngredientsTag, {
        product: productNew,
      });
      expect(ingredientsNew).toHaveLength(1);
      expect(ingredientsNew[0].value).toBe('test');
      expect(productNew.revision).toBe(1);

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

      // Check unchanged product has been "deleted"
      const foundOldProduct = await em.findOne(Product, {
        code: productIdUnchanged,
      });
      expect(foundOldProduct.obsolete).toBeNull();
      const ingredientsUnchanged = await em.find(ProductIngredientsTag, {
        product: foundOldProduct,
      });
      expect(ingredientsUnchanged[0].obsolete).toBeNull();

      const loadedTags = await app.get(TagService).getLoadedTags();
      expect(loadedTags).toHaveLength(
        Object.keys(ProductTagMap.MAPPED_TAGS).length,
      );
    });
  });

  it('incremental import should not update loaded tags', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: No loaded teams tag
      const em = app.get(EntityManager);
      await em.nativeDelete(LoadedTag, { id: 'teams_tags' });
      await em.flush();
      const importService = app.get(ImportService);

      // WHEN: Doing an incremental import from MongoDB
      const { products, productIdNew } = testProducts();
      mockMongoDB(products);
      await app.get(SettingsService).setLastModified(new Date());
      await importService.importFromMongo('');

      // THEN: Loaded tags is not updated
      const loadedTags = await app.get(TagService).getLoadedTags();
      expect(loadedTags).not.toContain('teams_tags');

      const productNew = await em.findOne(Product, { code: productIdNew });
      expect(productNew).toBeTruthy();
      expect(productNew.source).toBe(ProductSource.INCREMENTAL_LOAD);
    });
  });

  it('import with no change should not update the source', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: Product with data that matches MongoDB
      const em = app.get(EntityManager);
      const lastProcessed = new Date(2023, 1, 1);
      const { products, productIdExisting } = testProducts();
      em.create(Product, {
        code: productIdExisting,
        source: ProductSource.EVENT,
        lastProcessed: lastProcessed,
        lastUpdated: new Date(lastUpdated * 1000),
      });
      await em.flush();
      const importService = app.get(ImportService);

      // WHEN: Doing an incremental import from MongoDB
      mockMongoDB(products);
      await importService.importFromMongo('');

      // THEN: Source is not updated
      const productExisting = await em.findOne(Product, {
        code: productIdExisting,
      });
      expect(productExisting).toBeTruthy();
      expect(productExisting.source).toBe(ProductSource.EVENT);
      expect(productExisting.lastProcessed).toStrictEqual(lastProcessed);
    });
  });

  it('should start importing from the last import', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: lastUpdated setting already set
      const settings = app.get(SettingsService);
      const startFrom = new Date(2023, 1, 1);
      await settings.setLastModified(startFrom);
      const { products } = testProducts();
      const importService = app.get(ImportService);

      // WHEN: Doing an incremental import from MongoDB
      mockMongoDB(products);
      findCalls.length = 0;
      await importService.importFromMongo('');

      // THEN: Mongo find is called with the setting as a parameter
      expect(findCalls).toHaveLength(2); // Called for normal an obsolete prodocuts
      expect(findCalls[0][0].last_updated_t.$gt).toBe(
        Math.floor(startFrom.getTime() / 1000),
      );

      expect(await settings.getLastModified()).toStrictEqual(
        new Date(lastUpdated * 1000),
      );
    });
  });

  it('should cope with nul characters', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // WHEN: Importing data containing nul characters
      const { productIdNew } = testProducts();
      mockMongoDB([
        {
          // This one will be new
          code: productIdNew,
          last_updated_t: 1692032161,
          ingredients_tags: ['test \u0000 test2 \u0000 end'],
        },
      ]);
      await app.get(ImportService).importFromMongo();

      // THEN: Product should be loaded with nuls stripped
      const ingredientsNew = await app
        .get(EntityManager)
        .find(ProductIngredientsTag, {
          product: { code: productIdNew },
        });

      expect(ingredientsNew).toHaveLength(1);
      expect(ingredientsNew[0].value).toBe('test  test2  end');
    });
  });

  it('should set last_updated correctly if one product has an invalid date', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: products with invalid date
      const settings = app.get(SettingsService);
      const startFrom = new Date(2023, 1, 1);
      await settings.setLastModified(startFrom);
      const { products } = testProducts();
      const testData = [
        products[0],
        { ...products[1], last_updated_t: 'invalid' },
      ];
      const importService = app.get(ImportService);

      // WHEN: Doing an import from MongoDB
      mockMongoDB(testData);
      await importService.importFromMongo('');

      // THEN: The last modified date is set correctly
      expect(await settings.getLastModified()).toStrictEqual(
        new Date(lastUpdated * 1000),
      );
    });
  });

  it('should skip if already importing', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: Import already running
      const importService = app.get(ImportService);
      const { products } = testProducts();
      mockMongoDB(products);
      const firstImport = importService.importFromMongo();
      const warnSpy = jest.spyOn(importService['logger'], 'warn');

      // WHEN: Doing a second import
      await importService.importFromMongo();
      await firstImport;

      // THEN: Second import just logs a warning
      expect(warnSpy).toHaveBeenCalledTimes(1);
    });
  });

  it('should cope with duplicate product codes', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // WHEN: Importing data containing nul characters
      const { productIdNew } = testProducts();
      const productWithIngredients = {
        code: productIdNew,
        ingredients: [{ ingredient_text: 'test' }],
      };
      const duplicateProducts = [
        productWithIngredients,
        productWithIngredients,
      ];
      mockMongoDB(duplicateProducts);
      await app.get(ImportService).importFromMongo();

      // THEN: Product should be loaded with no duplicates
      const ingredientsNew = await app
        .get(EntityManager)
        .find(ProductIngredient, {
          product: { code: productIdNew },
        });

      expect(ingredientsNew).toHaveLength(1);
      expect(ingredientsNew[0].ingredientText).toBe('test');
    });
  });

  it('import from redis should always update product', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: Product with data that matches MongoDB
      const em = app.get(EntityManager);
      const lastProcessed = new Date(2023, 1, 1);
      const { products, productIdExisting } = testProducts();
      em.create(Product, {
        code: productIdExisting,
        source: ProductSource.INCREMENTAL_LOAD,
        lastProcessed: lastProcessed,
        lastUpdated: new Date(lastUpdated * 1000),
      });
      await em.flush();
      const importService = app.get(ImportService);

      // WHEN: Doing an event import
      mockMongoDB(products);
      await importService.importWithFilter(
        { code: { $in: [productIdExisting] } },
        ProductSource.EVENT,
      );

      // THEN: Source is updated
      const productExisting = await em.findOne(Product, {
        code: productIdExisting,
      });
      expect(productExisting).toBeTruthy();
      expect(productExisting.source).toBe(ProductSource.EVENT);
      expect(productExisting.lastProcessed).not.toStrictEqual(lastProcessed);
    });
  });
});

describe('scheduledImportFromMongo', () => {
  it('should do a full import if loaded tags arent complete', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      jest
        .spyOn(app.get(TagService), 'getLoadedTags')
        .mockImplementation(async () => []);
      const importSpy = jest
        .spyOn(importService, 'importFromMongo')
        .mockImplementation();
      await importService.scheduledImportFromMongo();
      expect(importSpy).toHaveBeenCalledTimes(1);
      expect(importSpy.mock.calls[0][0]).toBeUndefined();
    });
  });

  it('should do an incremental import if loaded tags are complete', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      jest
        .spyOn(app.get(TagService), 'getLoadedTags')
        .mockImplementation(async () =>
          Object.keys(ProductTagMap.MAPPED_TAGS).reverse(),
        );
      const importSpy = jest
        .spyOn(importService, 'importFromMongo')
        .mockImplementation();
      await importService.scheduledImportFromMongo();
      expect(importSpy).toHaveBeenCalledTimes(1);
      expect(importSpy.mock.calls[0][0]).toBe('');
    });
  });
});

describe('ProductTag', () => {
  it('should add class to tag array', async () => {
    await createTestingModule([DomainModule], async () => {
      expect(ProductTagMap.MAPPED_TAGS['categories_tags']).toBeTruthy();
    });
  });
});

describe('importWithFilter', () => {
  it('should not get an error with concurrent imports', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);

      // WHEN: Doing an incremental import from MongoDB
      const { products, productIdExisting, productIdNew } = testProducts();
      mockMongoDB(products);
      const imports = [];
      // Need more than 10 concurrent imports to start to see errors
      for (let i = 0; i < 11; i++) {
        imports.push(
          importService.importWithFilter(
            { code: { $in: [productIdExisting, productIdNew] } },
            ProductSource.EVENT,
          ),
        );
      }
      await Promise.all(imports);
    });
  });

  it('should flag products not in mongodb as deleted', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);

      // GIVEN: An existing product that doesn't exist in MongoDB
      const em = app.get(EntityManager);
      const productIdToDelete = randomCode();
      const productToDelete = em.create(Product, {
        code: productIdToDelete,
        source: ProductSource.FULL_LOAD,
        lastProcessed: new Date(2023, 1, 1),
        lastUpdated: new Date(lastUpdated * 1000),
      });
      em.create(ProductIngredientsTag, {
        product: productToDelete,
        value: 'old_ingredient',
      });
      await em.flush();

      const beforeImport = Date.now();
      // WHEN: Doing an incremental import from MongoDB where the id is mentioned
      const { products, productIdExisting, productIdNew } = testProducts();
      mockMongoDB(products);
      await importService.importWithFilter(
        { code: { $in: [productIdExisting, productIdNew, productIdToDelete] } },
        ProductSource.EVENT,
      );

      // THEN: Obsolete flag should get set to null
      const deletedProduct = await em.findOne(Product, {
        code: productIdToDelete,
      });
      const updatedProduct = await em.findOne(Product, {
        code: productIdExisting,
      });
      expect(deletedProduct.processId).toBe(updatedProduct.processId);
      expect(deletedProduct.lastProcessed.getTime()).toBeGreaterThanOrEqual(
        beforeImport,
      );
      expect(deletedProduct.source).toBe(ProductSource.EVENT);
      expect(updatedProduct.obsolete).toBe(false);

      const deletedTag = await em.findOne(ProductIngredientsTag, {
        product: deletedProduct,
      });
      expect(deletedTag.obsolete).toBeNull();
    });
  });
});

describe('getProcessId', () => {
  it('should return monotonically increasing numbers', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      const transactionId = await importService.getProcessId();

      expect(await importService.getProcessId()).toBeGreaterThan(transactionId);
    });
  });
});
