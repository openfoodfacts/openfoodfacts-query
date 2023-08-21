import { Test } from '@nestjs/testing';
import { DomainModule } from '../domain.module';
import { EntityManager, MikroORM, RequestContext } from '@mikro-orm/core';
import { Product } from '../entities/product';
import {
  ProductAdditivesTag,
  ProductIngredientsTag,
} from '../entities/product-tags';
import { QueryService } from './query.service';
import { randomCode } from '../../../test/test.helper';

describe('count', () => {
  it('should count the number of products with a tag', async () => {
    const app = await Test.createTestingModule({
      imports: [DomainModule],
    }).compile();

    const orm = app.get(MikroORM);
    try {
      await RequestContext.createAsync(orm.em, async () => {
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
    } finally {
      await orm.close();
    }
  });

  it('should count the number of products with a tag and not another tag', async () => {
    const app = await Test.createTestingModule({
      imports: [DomainModule],
    }).compile();

    const orm = app.get(MikroORM);
    try {
      await RequestContext.createAsync(orm.em, async () => {
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
    } finally {
      await orm.close();
    }
  });
});
