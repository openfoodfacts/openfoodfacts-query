import { DomainModule } from '../domain.module';
import { EntityManager } from '@mikro-orm/core';
import { Product } from '../entities/product';
import {
  ProductAdditivesTag,
  ProductIngredientsTag,
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
});
