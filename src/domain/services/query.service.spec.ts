import { DomainModule } from '../domain.module';
import { EntityManager } from '@mikro-orm/core';
import { Product } from '../entities/product';
import {
  ProductAdditivesTag,
  ProductAminoAcidsTag,
  ProductIngredientsTag,
  ProductNucleotidesTag,
  ProductOriginsTag,
} from '../entities/product-tags';
import { QueryService } from './query.service';
import { createTestingModule, randomCode } from '../../../test/test.helper';
import { UnprocessableEntityException } from '@nestjs/common';

describe('count', () => {
  it('should count the number of products with a tag', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const em = app.get(EntityManager);
      // Create some dummy products with a specific tag
      const tagValue = randomCode();
      em.create(ProductIngredientsTag, {
        product: em.create(Product, { code: randomCode() }),
        value: tagValue,
      });
      em.create(ProductIngredientsTag, {
        product: em.create(Product, { code: randomCode() }),
        value: tagValue,
      });
      await em.flush();
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        ingredients_tags: tagValue,
      });
      expect(response).toBe(2);
    });
  });

  it('should count the number of products with a tag and not another tag', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const em = app.get(EntityManager);
      // Create some dummy products with a specific tag
      const tagValue = randomCode();
      const notTagValue = randomCode();
      const productWithNotTag = em.create(Product, { code: randomCode() });
      em.create(ProductIngredientsTag, {
        product: productWithNotTag,
        value: tagValue,
      });
      em.create(ProductAdditivesTag, {
        product: productWithNotTag,
        value: notTagValue,
      });

      em.create(ProductIngredientsTag, {
        product: em.create(Product, { code: randomCode() }),
        value: tagValue,
      });
      await em.flush();

      const queryService = app.get(QueryService);
      const response = await queryService.count({
        ingredients_tags: tagValue,
        additives_tags: { $ne: notTagValue },
      });
      expect(response).toBe(1);
    });
  });

  it('should throw and unprocessable exception for an unknwon tag', async () => {
    await createTestingModule([DomainModule], async (app) => {
      try {
        await app.get(QueryService).count({ invalid_tag: 'x' });
        fail('should not get here');
      } catch (e) {
        expect(e).toBeInstanceOf(UnprocessableEntityException);
      }
    });
  });
  it('should cope with more than two filters', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue, neucleotideValue } =
        await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        origins_tags: originValue,
        amino_acids_tags: aminoValue,
        nucleotides_tags: neucleotideValue,
      });
      expect(response).toBe(1);
    });
  });
  it('should cope with no filters', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue, neucleotideValue } =
        await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count(null);
      expect(response).toBeGreaterThan(2);
    });
  });
});

describe('aggregate', () => {
  it('should group products with a tag', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.aggregate([
        { $match: {} },
        { $group: { _id: '$origins_tags' } },
      ]);
      const myTag = response.find((r) => r._id === originValue);
      expect(myTag).toBeTruthy();
      expect(parseInt(myTag.count)).toBe(3);
    });
  });

  it('should filter products when grouping', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.aggregate([
        { $match: { amino_acids_tags: aminoValue } },
        { $group: { _id: '$origins_tags' } },
      ]);
      const myTag = response.find((r) => r._id === originValue);
      expect(myTag).toBeTruthy();
      expect(parseInt(myTag.count)).toBe(2);
    });
  });

  it('should be able to do not filtering', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.aggregate([
        { $match: { amino_acids_tags: { $ne: aminoValue } } },
        { $group: { _id: '$origins_tags' } },
      ]);
      const myTag = response.find((r) => r._id === originValue);
      expect(myTag).toBeTruthy();
      expect(parseInt(myTag.count)).toBe(1);
    });
  });

  it('should be able to just count', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const queryService = app.get(QueryService);
      const query = [
        { $match: {} },
        { $group: { _id: '$origins_tags' } },
        { $count: 1 },
      ];
      const beforeResponse = await queryService.aggregate(query);
      const beforeCount = parseInt(beforeResponse['origins_tags']);

      await createTestTags(app);
      const response = await queryService.aggregate(query);
      expect(parseInt(response['origins_tags'])).toBe(beforeCount + 1);
    });
  });

  it('should cope with multiple filters', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue, neucleotideValue } =
        await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.aggregate([
        {
          $match: {
            amino_acids_tags: aminoValue,
            nucleotides_tags: neucleotideValue,
          },
        },
        { $group: { _id: '$origins_tags' } },
      ]);
      const myTag = response.find((r) => r._id === originValue);
      expect(myTag).toBeTruthy();
      expect(parseInt(myTag.count)).toBe(1);
    });
  });
});

describe('select', () => {
  it('should return matching products', async () =>{
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue, neucleotideValue, product1, product2, product3 } =
        await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.select({
        amino_acids_tags: aminoValue,
      });
      expect(response).toHaveLength(2);
      const p1 = response.find((r) => r.code === product1.code);
      expect(p1).toBeTruthy();
    });
  });
});

async function createTestTags(app) {
  const em = app.get(EntityManager);
  // Create some dummy products with a specific tag
  const product1 = em.create(Product, { code: randomCode() });
  const product2 = em.create(Product, { code: randomCode() });
  const product3 = em.create(Product, { code: randomCode() });
  // Using origins and amino acids as they are smaller than most
  const originValue = randomCode();
  const aminoValue = randomCode();
  const neucleotideValue = randomCode();

  // Matrix for testing
  // Product  | Origin | AminoAcid | Neucleotide
  // Product1 |   x    |     x     |      x
  // Product2 |   x    |     x     |
  // Product3 |   x    |           |      x

  em.create(ProductOriginsTag, {
    product: product1,
    value: originValue,
  });
  em.create(ProductOriginsTag, {
    product: product2,
    value: originValue,
  });
  em.create(ProductOriginsTag, {
    product: product3,
    value: originValue,
  });

  em.create(ProductAminoAcidsTag, {
    product: product1,
    value: aminoValue,
  });
  em.create(ProductAminoAcidsTag, {
    product: product2,
    value: aminoValue,
  });

  em.create(ProductNucleotidesTag, {
    product: product1,
    value: neucleotideValue,
  });
  em.create(ProductNucleotidesTag, {
    product: product3,
    value: neucleotideValue,
  });

  await em.flush();
  return { originValue, aminoValue, neucleotideValue, product1, product2, product3 };
}
