import { DomainModule } from '../domain.module';
import { ImportService } from './import.service';
import { EntityManager } from '@mikro-orm/core';
import { Product } from '../entities/product';
import { ProductIngredientsTag } from '../entities/product-tags';
import { createTestingModule, randomCode } from '../../../test/test.helper';
import { TagService } from './tag.service';
import { LoadedTag } from '../entities/loaded-tag';
import { ProductTagMap } from '../entities/product-tag-map';
import { ProductSource } from '../enums/product-source';
import { SettingsService } from './settings.service';

let index = 0;
const lastModified = 1692032161;

function testProducts() {
  const productIdNew = randomCode();
  const productIdExisting = randomCode();
  const products = [
    {
      // This one will be new
      code: productIdNew,
      last_modified_t: lastModified,
      ingredients_tags: ['test'],
    },
    {
      // This one will already exist
      code: productIdExisting,
      last_modified_t: lastModified,
      ingredients_tags: ['new_ingredient', 'old_ingredient'],
    },
  ];
  return { products, productIdExisting, productIdNew };
}

const findMock = jest.fn((filter, projection) => ({
  next: async () => {
    return index++ <= mockedProducts.length ? mockedProducts[index - 1] : null;
  },
  close: jest.fn(),
}));

jest.mock('mongodb', () => {
  return {
    MongoClient: jest.fn(() => ({
      connect: jest.fn(),
      db: () => ({
        collection: () => ({
          find: findMock,
        }),
      }),
      close: jest.fn(),
    })),
  };
});

let mockedProducts = [];
function mockMongoDB(productList) {
  index = 0;
  mockedProducts = productList;
}

// Import tests can sometimes take a little time in GitHub
jest.setTimeout(10000);

describe('importFromMongo', () => {
  it('should import a new product update existing products and delete missing products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // To see Mikro-ORM log output you need to make sure NestJS isn't using it's TestLogger
      // And also uncomment the debug setting in mikro-orm.config.ts
      // app.useLogger(new Logger());

      const importService = app.get(ImportService);
      const deleteMock = (importService.deleteOtherProducts = jest.fn());

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

      // THEN: New product is addeded, updated product is updated and other product is unchanged
      expect(deleteMock).toHaveBeenCalledTimes(1);
      let updateId = deleteMock.mock.calls[0][0];
      // Re-format updateId the way Postgres provides it
      updateId = `${updateId.substring(0, 8)}-${updateId.substring(
        8,
        12,
      )}-${updateId.substring(12, 16)}-${updateId.substring(
        16,
        20,
      )}-${updateId.substring(20)}`.toLowerCase();
      const productNew = await em.findOne(Product, { code: productIdNew });
      expect(productNew).toBeTruthy();
      expect(productNew.lastUpdateId).toBe(updateId);
      expect(productNew.source).toBe(ProductSource.FULL_LOAD);
      expect(productNew.lastUpdated.getTime()).toBeGreaterThanOrEqual(start);
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

      // We have mocked the delete of other products so just check the other product
      // does not have the same update id as those imported
      const foundOldProduct = await em.findOne(Product, {
        code: productIdUnchanged,
      });
      expect(foundOldProduct.lastUpdateId).not.toBe(updateId);

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
      (await app.get(SettingsService).get()).lastModified = new Date();
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
      const lastUpdated = new Date(2023, 1, 1);
      const { products, productIdExisting } = testProducts();
      em.create(Product, {
        code: productIdExisting,
        data: products[1],
        source: ProductSource.EVENT,
        lastUpdated: lastUpdated,
      });
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
      expect(productExisting.lastUpdated).toStrictEqual(lastUpdated);
    });
  });

  it('should start importing from the last import', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // GIVEN: lastModified setting already set
      const settings = await app.get(SettingsService).get();
      const startFrom = new Date(2023, 1, 1);
      settings.lastModified = startFrom;
      const { products } = testProducts();
      const importService = app.get(ImportService);

      // WHEN: Doing an incremental import from MongoDB
      mockMongoDB(products);
      findMock.mockClear();
      await importService.importFromMongo('');

      // THEN: Mongo find is called with the setting as a parameter
      expect(findMock).toHaveBeenCalledTimes(2); // Called for normal an obsolete prodocuts
      expect(findMock.mock.calls[0][0].last_modified_t.$gt).toBe(
        Math.floor(startFrom.getTime() / 1000),
      );

      expect(settings.lastModified).toStrictEqual(
        new Date(lastModified * 1000),
      );
    });
  });

  it('should cope with nul charactes', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // WHEN: Impoting data containing nul characters
      const { productIdNew } = testProducts();
      mockMongoDB([
        {
          // This one will be new
          code: productIdNew,
          last_modified_t: 1692032161,
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
    await createTestingModule([DomainModule], async (app) => {
      expect(ProductTagMap.MAPPED_TAGS['categories_tags']).toBeTruthy();
    });
  });
});
