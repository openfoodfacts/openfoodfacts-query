import { DomainModule } from '../domain.module';
import { EntityManager } from '@mikro-orm/core';
import { Product } from '../entities/product';
import {
  ProductAdditivesTag,
  ProductAminoAcidsTag,
  ProductBrandsTag,
  ProductIngredientsTag,
  ProductNucleotidesTag,
  ProductOriginsTag,
} from '../entities/product-tags';
import { QueryService } from './query.service';
import { createTestingModule, randomCode } from '../../../test/test.helper';
import { UnprocessableEntityException } from '@nestjs/common';
import { LoadedTag } from '../entities/loaded-tag';

// Tests can sometimes take a little time in GitHub
jest.setTimeout(10000);

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
      em.create(ProductBrandsTag, {
        product: productWithNotTag,
        value: tagValue,
      });
      em.create(ProductAdditivesTag, {
        product: productWithNotTag,
        value: notTagValue,
      });

      em.create(ProductBrandsTag, {
        product: em.create(Product, { code: randomCode() }),
        value: tagValue,
      });
      await em.flush();

      const queryService = app.get(QueryService);
      const response = await queryService.count({
        brands_tags: tagValue,
        additives_tags: { $ne: notTagValue },
      });
      expect(response).toBe(1);
    });
  });

  it('should count the number of products without a specified tag', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { aminoValue, originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        amino_acids_tags: { $ne: aminoValue },
        origins_tags: originValue, // Need at least one other criteria to avoid products from other tests
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

  it('should throw and unprocessable exception for a tag that hasnt been loaded', async () => {
    await createTestingModule([DomainModule], async (app) => {
      try {
        const em = app.get(EntityManager);
        await em.nativeDelete(LoadedTag, { id: 'ingredients_tags' });
        await em.flush();
        await app.get(QueryService).count({ ingredients_tags: 'x' });
        fail('should not get here');
      } catch (e) {
        expect(e).toBeInstanceOf(UnprocessableEntityException);
      }
    });
  });

  it('should throw and unprocessable exception for an unrecognised value object', async () => {
    await createTestingModule([DomainModule], async (app) => {
      try {
        await app.get(QueryService).count({ origins_tags: { $unknown: 'x' } });
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
      await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count(null);
      expect(response).toBeGreaterThan(2);
    });
  });

  it('should be able to count obsolete products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count(
        {
          origins_tags: originValue,
        },
        true,
      );
      expect(response).toBe(1);
    });
  });

  it('should be able to count not obsolete products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count(
        {
          origins_tags: originValue,
        },
        false,
      );
      expect(response).toBe(3);
    });
  });

  it('should cope with a $all filter', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { aminoValue, aminoValue2 } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        amino_acids_tags: { $all: [aminoValue, aminoValue2] },
      });
      expect(response).toBe(1);
    });
  });

  it('should cope with a $and filter', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { aminoValue, aminoValue2 } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        $and: [
          { amino_acids_tags: aminoValue },
          { amino_acids_tags: aminoValue2 },
        ],
      });
      expect(response).toBe(1);
    });
  });

  it('should cope with an $in value', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { aminoValue, aminoValue2 } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        amino_acids_tags: { $in: [aminoValue, aminoValue2] },
      });
      expect(response).toBe(3);
    });
  });

  it('should throw an unprocessable exception if an $in contains an array', async () => {
    await createTestingModule([DomainModule], async (app) => {
      try {
        await app
          .get(QueryService)
          .count({ origins_tags: { $in: ['a', ['b', 'c']] } });
        fail('should not get here');
      } catch (e) {
        expect(e).toBeInstanceOf(UnprocessableEntityException);
      }
    });
  });

  it('should cope with an $in unknown value', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        origins_tags: originValue,
        nucleotides_tags: { $in: [null, []] },
      });
      expect(response).toBe(1);
    });
  });

  it('should cope with an $in unknown value on a product field', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        origins_tags: originValue,
        creator: { $in: [null, []] },
      });
      expect(response).toBe(1);
    });
  });

  it('should cope with $nin', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue, aminoValue2 } = await createTestTags(
        app,
      );
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        origins_tags: originValue,
        amino_acids_tags: { $nin: [aminoValue, aminoValue2] },
      });
      expect(response).toBe(0);
    });
  });

  it('should cope with $nin unknown', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        origins_tags: originValue,
        nucleotides_tags: { $nin: [null, []] },
      });
      expect(response).toBe(2);
    });
  });

  it('should cope with $nin unknown value on a product field', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.count({
        origins_tags: originValue,
        creator: { $nin: [null, []] },
      });
      expect(response).toBe(2);
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

  it('should filter products when grouping by a product field', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { aminoValue, creatorValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.aggregate([
        { $match: { amino_acids_tags: aminoValue } },
        { $group: { _id: '$creator' } },
      ]);
      const myTag = response.find((r) => r._id === creatorValue);
      expect(myTag).toBeTruthy();
      expect(parseInt(myTag.count)).toBe(1);
    });
  });

  it('should group products when filtering by a product field', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { aminoValue, creatorValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.aggregate([
        { $match: { creator: creatorValue } },
        { $group: { _id: '$amino_acids_tags' } },
      ]);
      const myTag = response.find((r) => r._id === aminoValue);
      expect(myTag).toBeTruthy();
      expect(parseInt(myTag.count)).toBe(1);
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

  it('should be able to group obsolete products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.aggregate(
        [{ $match: {} }, { $group: { _id: '$origins_tags' } }],
        true,
      );
      const myTag = response.find((r) => r._id === originValue);
      expect(myTag).toBeTruthy();
      expect(parseInt(myTag.count)).toBe(1);
    });
  });
});

describe('select', () => {
  it('should return matching products', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { aminoValue, product1, product4 } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.select({
        amino_acids_tags: aminoValue,
      });
      expect(response).toHaveLength(3); // Includes obsolete
      const p1 = response.find((r) => r.code === product1.code);
      expect(p1).toBeTruthy();
      expect(p1.obsolete).toBe(false);

      const p4 = response.find((r) => r.code === product4.code);
      expect(p4).toBeTruthy();
      expect(p4.obsolete).toBe(true);
    });
  });

  it('should cope with $nin', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const { originValue, aminoValue, product3 } = await createTestTags(app);
      const queryService = app.get(QueryService);
      const response = await queryService.select({
        origins_tags: originValue,
        amino_acids_tags: { $nin: [aminoValue] },
      });
      expect(response).toHaveLength(1);
      expect(response[0].code).toBe(product3.code);
    });
  });
});

async function createTestTags(app) {
  const em = app.get(EntityManager);

  // Using origins and amino acids as they are smaller than most
  const originValue = randomCode();
  const aminoValue = randomCode();
  const aminoValue2 = randomCode();
  const neucleotideValue = randomCode();
  const creatorValue = randomCode();

  // Create some dummy products with a specific tag
  const product1 = em.create(Product, { code: randomCode() });
  const product2 = em.create(Product, {
    code: randomCode(),
    creator: creatorValue,
  });
  const product3 = em.create(Product, {
    code: randomCode(),
    creator: creatorValue,
  });
  const product4 = em.create(Product, { code: randomCode(), obsolete: true });

  // Matrix for testing
  // Product  | Origin | AminoAcid | AminoAcid2 | Neucleotide | Obsolete | Creator
  // Product1 |   x    |     x     |            |      x      |          |
  // Product2 |   x    |     x     |     x      |             |          |    x
  // Product3 |   x    |           |     x      |      x      |          |    x
  // Product4 |   x    |     x     |            |      x      |    x     |

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
  em.create(ProductOriginsTag, {
    product: product4,
    value: originValue,
    obsolete: true,
  });

  em.create(ProductAminoAcidsTag, {
    product: product1,
    value: aminoValue,
  });
  em.create(ProductAminoAcidsTag, {
    product: product2,
    value: aminoValue,
  });
  em.create(ProductAminoAcidsTag, {
    product: product4,
    value: aminoValue,
    obsolete: true,
  });

  em.create(ProductAminoAcidsTag, {
    product: product2,
    value: aminoValue2,
  });
  em.create(ProductAminoAcidsTag, {
    product: product3,
    value: aminoValue2,
  });

  em.create(ProductNucleotidesTag, {
    product: product1,
    value: neucleotideValue,
  });
  em.create(ProductNucleotidesTag, {
    product: product3,
    value: neucleotideValue,
  });
  em.create(ProductNucleotidesTag, {
    product: product4,
    value: neucleotideValue,
    obsolete: true,
  });

  await em.flush();
  return {
    originValue,
    aminoValue,
    aminoValue2,
    neucleotideValue,
    creatorValue,
    product1,
    product2,
    product3,
    product4,
  };
}
