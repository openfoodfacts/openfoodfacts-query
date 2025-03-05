from uuid import uuid4
from query.db import Database
from query.models.filter import Filter, Qualify
import query.services.query as query
from query.tables.product import create_product
from query.tables.product_tags import create_tag
from tests.helper import random_code


async def test_count_should_count_the_number_of_products_with_a_tag():
    async with Database() as connection:
        ingredient_value = random_code()
        # Create 2 products with the tag we want
        await create_tag(connection, 'ingredients_tags', await create_product(connection, random_code()), ingredient_value)
        await create_tag(connection, 'ingredients_tags', await create_product(connection, random_code()), ingredient_value)
        # Create another with a tag we don't want
        await create_tag(connection, 'ingredients_tags', await create_product(connection, random_code()), random_code())

    count = await query.count(Filter(ingredients_tags = ingredient_value))
    assert count == 2
                             
async def test_count_should_count_the_number_of_products_with_a_tag_and_not_another_tag():
    async with Database() as connection:
        # Create some dummy products with a specific tag
        tag_value = random_code()
        not_tag_value = random_code()

        # Product with the tag we don't want
        product_with_not_tag = await create_product(connection, random_code())
        await create_tag(connection, 'brands_tags', product_with_not_tag, tag_value)
        await create_tag(connection, 'additives_tags', product_with_not_tag, not_tag_value)
        
        # Product with just the tag we want
        await create_tag(connection, 'brands_tags', await create_product(connection, random_code()), tag_value)
    
    response = await query.count(Filter(brands_tags = tag_value, additives_tags = Qualify(ne = not_tag_value)))
    assert response == 1

#   it('should count the number of products without a specified tag', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { aminoValue, originValue } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         amino_acids_tags: { $ne: aminoValue },
#         origins_tags: originValue, // Need at least one other criteria to avoid products from other tests
#       });
#       expect(response).toBe(1);
#     });
#   });

#   it('should throw and unprocessable exception for an unknwon tag', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       try {
#         await app.get(QueryService).count({ invalid_tag: 'x' });
#         fail('should not get here');
#       } catch (e) {
#         expect(e).toBeInstanceOf(UnprocessableEntityException);
#       }
#     });
#   });

#   it('should throw and unprocessable exception for a tag that hasnt been loaded', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       try {
#         const em = app.get(EntityManager);
#         await em.nativeDelete(LoadedTag, { id: 'ingredients_tags' });
#         await em.flush();
#         await app.get(QueryService).count({ ingredients_tags: 'x' });
#         fail('should not get here');
#       } catch (e) {
#         expect(e).toBeInstanceOf(UnprocessableEntityException);
#       }
#     });
#   });

#   it('should throw and unprocessable exception for an unrecognised value object', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       try {
#         // @ts-expect-error Only certain operators are supported
#         await app.get(QueryService).count({ origins_tags: { $unknown: 'x' } });
#         fail('should not get here');
#       } catch (e) {
#         expect(e).toBeInstanceOf(UnprocessableEntityException);
#       }
#     });
#   });

#   it('should cope with more than two filters', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue, aminoValue, neucleotideValue } =
#         await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         origins_tags: originValue,
#         amino_acids_tags: aminoValue,
#         nucleotides_tags: neucleotideValue,
#       });
#       expect(response).toBe(1);
#     });
#   });

#   it('should cope with no filters', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count(null);
#       expect(response).toBeGreaterThan(2);
#     });
#   });

#   it('should be able to count obsolete products', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count(
#         {
#           origins_tags: originValue,
#         },
#         true,
#       );
#       expect(response).toBe(1);
#     });
#   });

#   it('should be able to count not obsolete products', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count(
#         {
#           origins_tags: originValue,
#         },
#         false,
#       );
#       expect(response).toBe(3);
#     });
#   });

#   it('should cope with a $all filter', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { aminoValue, aminoValue2 } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         amino_acids_tags: { $all: [aminoValue, aminoValue2] },
#       });
#       expect(response).toBe(1);
#     });
#   });

#   it('should cope with a $and filter', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { aminoValue, aminoValue2 } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         $and: [
#           { amino_acids_tags: aminoValue },
#           { amino_acids_tags: aminoValue2 },
#         ],
#       });
#       expect(response).toBe(1);
#     });
#   });

#   it('should cope with an $in value', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { aminoValue, aminoValue2 } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         amino_acids_tags: { $in: [aminoValue, aminoValue2] },
#       });
#       expect(response).toBe(3);
#     });
#   });

#   it('should throw an unprocessable exception if an $in contains an array', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       try {
#         await app
#           .get(QueryService)
#           // @ts-expect-error $in should only include simple type
#           .count({ origins_tags: { $in: ['a', ['b', 'c']] } });
#         fail('should not get here');
#       } catch (e) {
#         expect(e).toBeInstanceOf(UnprocessableEntityException);
#       }
#     });
#   });

#   it('should cope with an $in unknown value', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         origins_tags: originValue,
#         nucleotides_tags: { $in: [null, []] },
#       });
#       expect(response).toBe(1);
#     });
#   });

#   it('should cope with an $in unknown value on a product field', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         origins_tags: originValue,
#         creator: { $in: [null, []] },
#       });
#       expect(response).toBe(1);
#     });
#   });

#   it('should cope with $nin', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue, aminoValue, aminoValue2 } = await createTestTags(
#         app,
#       );
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         origins_tags: originValue,
#         amino_acids_tags: { $nin: [aminoValue, aminoValue2] },
#       });
#       expect(response).toBe(0);
#     });
#   });

#   it('should cope with $nin unknown', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         origins_tags: originValue,
#         nucleotides_tags: { $nin: [null, []] },
#       });
#       expect(response).toBe(2);
#     });
#   });

#   it('should cope with $nin unknown value on a product field', async () => {
#     await createTestingModule([DomainModule], async (app) => {
#       const { originValue } = await createTestTags(app);
#       const queryService = app.get(QueryService);
#       const response = await queryService.count({
#         origins_tags: originValue,
#         creator: { $nin: [null, []] },
#       });
#       expect(response).toBe(2);
#     });
#   });
# });

