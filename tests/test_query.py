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
        Filter(brands_tags=tag_value, additives_tags=Qualify(qualify_ne=not_tag_value))
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
                amino_acids_tags=Qualify(qualify_ne=tags.amino_value),
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
            Filter(
                amino_acids_tags=Qualify(
                    qualify_all=[tags.amino_value, tags.amino_value2]
                )
            )
        )
        assert response == 1


async def test_count_should_cope_with_an_and_filter():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                qualify_and=[
                    Filter(amino_acids_tags=tags.amino_value),
                    Filter(amino_acids_tags=tags.amino_value2),
                ]
            )
        )
        assert response == 1


async def test_count_should_cope_with_an_in_value():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                amino_acids_tags=Qualify(
                    qualify_in=[tags.amino_value, tags.amino_value2]
                )
            )
        )
        assert response == 3


# TODO: Check this is an HTTP_422_UNPROCESSABLE_ENTITY status in the controller
async def test_count_should_throw_an_unprocessable_exception_if_an_in_contains_a_sub_array():
    with pytest.raises(ValidationError) as e:
        await query.count(Filter(origins_tags=Qualify(qualify_in=["a", ["b", "c"]])))
    main_error = e.value.errors()[0]
    assert main_error["type"] == "string_type"
    assert main_error["loc"][0] == "qualify_in"


async def test_count_should_cope_with_an_in_unknown_value():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                nucleotides_tags=Qualify(qualify_in=[None, []]),
            )
        )
        assert response == 1


# TODO: Add a few more product field tests

async def test_count_should_count_with_a_product_field():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                creator=tags.creator_value,
            )
        )
        assert response == 2


async def test_count_should_count_with_in_on_a_product_field():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                creator=Qualify(qualify_in=[tags.creator_value]),
            )
        )
        assert response == 2


async def test_count_should_count_with_nin_on_a_product_field():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                creator=Qualify(qualify_nin=[tags.creator_value]),
            )
        )
        assert response == 1


async def test_count_should_cope_with_an_in_unknown_value_on_a_product_field():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                creator=Qualify(qualify_in=[None, []]),
            )
        )
        assert response == 1


async def test_count_should_cope_with_nin():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                amino_acids_tags=Qualify(
                    qualify_nin=[tags.amino_value, tags.amino_value2]
                ),
            )
        )
        assert response == 0


async def test_count_should_cope_with_nin_unknown():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                nucleotides_tags=Qualify(qualify_nin=[None, []]),
            )
        )
        assert response == 2


async def test_count_should_cope_with_nin_unknown_on_a_product_field():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.count(
            Filter(
                origins_tags=tags.origin_value,
                creator=Qualify(qualify_nin=[None, []]),
            )
        )
        assert response == 2
