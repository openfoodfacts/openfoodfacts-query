from unittest.mock import patch
from uuid import uuid4

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError
import pytest
from query.db import Database
from query.models.filter import Filter, Qualify
from query.models.product import Product
import query.services.query as query
from query.tables.product import create_product
from query.tables.product_tags import create_tag
from tests.helper import random_code


async def create_random_product(connection, creator=None, obsolete=False):
    return await create_product(
        connection, Product(code=random_code(), creator=creator, obsolete=obsolete)
    )


async def test_count_should_count_the_number_of_products_with_a_tag():
    async with Database() as connection:
        ingredient_value = random_code()
        # Create 2 products with the tag we want
        await create_tag(
            connection,
            "ingredients_tags",
            await create_random_product(connection),
            ingredient_value,
        )
        await create_tag(
            connection,
            "ingredients_tags",
            await create_random_product(connection),
            ingredient_value,
        )
        # Create another with a tag we don't want
        await create_tag(
            connection,
            "ingredients_tags",
            await create_random_product(connection),
            random_code(),
        )

    count = await query.count(Filter(ingredients_tags=ingredient_value))
    assert count == 2


async def test_count_should_count_the_number_of_products_with_a_tag_and_not_another_tag():
    async with Database() as connection:
        # Create some dummy products with a specific tag
        tag_value = random_code()
        not_tag_value = random_code()

        # Product with the tag we don't want
        product_with_not_tag = await create_random_product(connection)
        await create_tag(connection, "brands_tags", product_with_not_tag, tag_value)
        await create_tag(
            connection, "additives_tags", product_with_not_tag, not_tag_value
        )

        # Product with just the tag we want
        await create_tag(
            connection,
            "brands_tags",
            await create_random_product(connection),
            tag_value,
        )

    response = await query.count(
        Filter(brands_tags=tag_value, additives_tags=Qualify(ne=not_tag_value))
    )
    assert response == 1


class TestTags(BaseModel):
    origin_value: str
    amino_value: str
    amino_value2: str
    neucleotide_value: str
    creator_value: str
    product1: int
    product2: int
    product3: int
    product4: int


async def create_test_tags(connection):
    # Using origins and amino acids as they are smaller than most
    origin_value = random_code()
    amino_value = random_code()
    amino_value2 = random_code()
    neucleotide_value = random_code()
    creator_value = random_code()

    # Create some dummy products with a specific tag
    product1 = await create_random_product(connection)
    product2 = await create_random_product(connection, creator_value)
    product3 = await create_random_product(connection, creator_value)
    product4 = await create_random_product(connection, obsolete=True)

    # Matrix for testing
    # Product  | Origin | AminoAcid | AminoAcid2 | Neucleotide | Obsolete | Creator
    # Product1 |   x    |     x     |            |      x      |          |
    # Product2 |   x    |     x     |     x      |             |          |    x
    # Product3 |   x    |           |     x      |      x      |          |    x
    # Product4 |   x    |     x     |            |      x      |    x     |

    await create_tag(connection, "origins_tags", product1, origin_value)
    await create_tag(connection, "origins_tags", product2, origin_value)
    await create_tag(connection, "origins_tags", product3, origin_value)
    await create_tag(connection, "origins_tags", product4, origin_value, True)
    await create_tag(connection, "amino_acids_tags", product1, amino_value)
    await create_tag(connection, "amino_acids_tags", product2, amino_value)
    await create_tag(connection, "amino_acids_tags", product2, amino_value2)
    await create_tag(connection, "amino_acids_tags", product3, amino_value2)
    await create_tag(connection, "amino_acids_tags", product4, amino_value, True)
    await create_tag(connection, "nucleotides_tags", product1, neucleotide_value)
    await create_tag(connection, "nucleotides_tags", product3, neucleotide_value)
    await create_tag(connection, "nucleotides_tags", product4, neucleotide_value, True)

    return TestTags(
        origin_value=origin_value,
        amino_value=amino_value,
        amino_value2=amino_value2,
        neucleotide_value=neucleotide_value,
        creator_value=creator_value,
        product1=product1,
        product2=product2,
        product3=product3,
        product4=product4,
    )


async def test_count_should_count_the_number_of_products_without_a_specified_tag():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                amino_acids_tags=Qualify(ne=tags.amino_value),
                # need at least one other criteria to avoid products from other tests
                origins_tags=tags.origin_value,
            )
        )
        assert response == 1


# TODO: Check this is an HTTP_422_UNPROCESSABLE_ENTITY status in the controller
async def test_count_should_throw_an_exception_for_an_unknown_tag():
    with pytest.raises(ValidationError) as e:
        await query.count(Filter(invalid_tags="x"))
    main_error = e.value.errors()[0]
    assert main_error["type"] == "extra_forbidden"
    assert main_error["loc"][0] == "invalid_tags"


@patch("query.services.query.get_loaded_tags", return_value=["dummy_tag"])
async def test_count_should_throw_an_unprocessable_exception_for_a_tag_that_hasnt_been_loaded(
    get_loaded_tags_mock,
):
    with pytest.raises(HTTPException) as e:
        await query.count(Filter(ingredients_tags="x"))
    assert get_loaded_tags_mock.called
    assert e.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "ingredients_tags" in repr(e.value.detail)


# TODO: Check this is an HTTP_422_UNPROCESSABLE_ENTITY status in the controller
async def test_count_should_throw_and_unprocessable_exception_for_an_unrecognised_value_object():
    with pytest.raises(ValidationError) as e:
        await query.count(Filter(ingredients_tags=Qualify(unknown="x")))
    main_error = e.value.errors()[0]
    assert main_error["type"] == "extra_forbidden"
    assert main_error["loc"][0] == "unknown"


async def test_count_should_cope_with_more_than_two_filters():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                amino_acids_tags=tags.amino_value,
                nucleotides_tags=tags.neucleotide_value,
            )
        )
        assert response == 1


async def test_count_should_cope_with_an_empty_filter():
    async with Database() as connection:
        await create_test_tags(connection)
        response = await query.count(Filter())
        assert response > 2


async def test_count_should_cope_with_no_filters():
    async with Database() as connection:
        await create_test_tags(connection)
        response = await query.count()
        assert response > 2


async def test_count_should_be_able_to_count_obsolete_products():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(Filter(origins_tags=tags.origin_value), True)
        assert response == 1


async def test_count_should_be_able_to_count_not_obsolete_products():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(Filter(origins_tags=tags.origin_value), False)
        assert response == 3


async def test_count_should_cope_with_an_all_filter():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(amino_acids_tags=Qualify(all=[tags.amino_value, tags.amino_value2]))
        )
        assert response == 1

async def test_count_should_cope_with_an_and_filter():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(filter_and=[Filter(amino_acids_tags=tags.amino_value), Filter(amino_acids_tags=tags.amino_value2)])
        )
        assert response == 1
#     await create_testing_module([domain_module], async (app) => {
#       const { amino_value, amino_value2 } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.count({
#         $and: [
#           { amino_acids_tags: amino_value },
#           { amino_acids_tags: amino_value2 },
#         ],
#       });
#       expect(response).to_be(1);
#     });
#   });

#   it('should cope with an $in value', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { amino_value, amino_value2 } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.count({
#         amino_acids_tags: { $in: [amino_value, amino_value2] },
#       });
#       expect(response).to_be(3);
#     });
#   });

#   it('should throw an unprocessable exception if an $in contains an array', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       try {
#         await app
#           .get(query_service)
#           // @ts-expect-error $in should only include simple type
#           .count({ origins_tags: { $in: ['a', ['b', 'c']] } });
#         fail('should not get here');
#       } catch (e) {
#         expect(e).to_be_instance_of(unprocessable_entity_exception);
#       }
#     });
#   });

#   it('should cope with an $in unknown value', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.count({
#         origins_tags: origin_value,
#         nucleotides_tags: { $in: [null, []] },
#       });
#       expect(response).to_be(1);
#     });
#   });

#   it('should cope with an $in unknown value on a product field', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.count({
#         origins_tags: origin_value,
#         creator: { $in: [null, []] },
#       });
#       expect(response).to_be(1);
#     });
#   });

#   it('should cope with $nin', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value, amino_value, amino_value2 } = await create_test_tags(
#         app,
#       );
#       const query_service = app.get(query_service);
#       const response = await query_service.count({
#         origins_tags: origin_value,
#         amino_acids_tags: { $nin: [amino_value, amino_value2] },
#       });
#       expect(response).to_be(0);
#     });
#   });

#   it('should cope with $nin unknown', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.count({
#         origins_tags: origin_value,
#         nucleotides_tags: { $nin: [null, []] },
#       });
#       expect(response).to_be(2);
#     });
#   });

#   it('should cope with $nin unknown value on a product field', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.count({
#         origins_tags: origin_value,
#         creator: { $nin: [null, []] },
#       });
#       expect(response).to_be(2);
#     });
#   });
# });
