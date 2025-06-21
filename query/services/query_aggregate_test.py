import pytest
from pydantic import ValidationError

from query.tables.product_nutrient import NUTRIENT_TAG

from ..database import get_transaction
from ..models.query import Filter, GroupStage, Qualify, Stage
from ..services import query
from ..services.query_count_test import create_test_tags


async def test_group_products_with_a_tag():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [Stage(match=Filter()), Stage(group=GroupStage(id="$origins_tags"))]
    )
    my_result = [result for result in response if result.id == tags.origin_value]
    assert len(my_result) == 1
    assert my_result[0].count == 3


async def test_filter_products_when_grouping():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(match=Filter(amino_acids_tags=tags.amino_value)),
            Stage(group=GroupStage(id="$origins_tags")),
        ]
    )
    my_result = [result for result in response if result.id == tags.origin_value]
    assert len(my_result) == 1
    assert my_result[0].count == 2


async def test_filter_products_when_grouping_by_a_product_field():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(match=Filter(amino_acids_tags=tags.amino_value)),
            Stage(group=GroupStage(id="$creator")),
        ]
    )
    my_result = [result for result in response if result.id == tags.creator_value]
    assert len(my_result) == 1
    assert my_result[0].count == 1


async def test_group_products_when_filtering_by_a_product_field():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(match=Filter(creator=tags.creator_value)),
            Stage(group=GroupStage(id="$amino_acids_tags")),
        ]
    )

    assert len(response) == 2
    assert response[0].count == 2
    assert response[0].id == tags.amino_value2
    assert response[1].count == 1
    assert response[1].id == tags.amino_value


async def test_limit():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(match=Filter(creator=tags.creator_value)),
            Stage(group=GroupStage(id="$amino_acids_tags")),
            Stage(limit=1),
        ]
    )

    assert len(response) == 1
    assert response[0].count == 2
    assert response[0].id == tags.amino_value2


async def test_skip():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(match=Filter(creator=tags.creator_value)),
            Stage(group=GroupStage(id="$amino_acids_tags")),
            Stage(limit=1),
            Stage(skip=1),
        ]
    )

    assert len(response) == 1
    assert response[0].count == 1
    assert response[0].id == tags.amino_value


async def test_able_to_do_not_filtering():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(match=Filter(amino_acids_tags=Qualify(qualify_ne=tags.amino_value))),
            Stage(group=GroupStage(id="$origins_tags")),
        ]
    )
    my_result = [result for result in response if result.id == tags.origin_value]
    assert len(my_result) == 1
    assert my_result[0].count == 1


async def test_able_to_just_count():
    async with get_transaction() as transaction:
        await create_test_tags(transaction)

    aggregate_query = [
        Stage(match=Filter()),
        Stage(group=GroupStage(id="$origins_tags")),
        Stage(count=1),
    ]
    before_response = await query.aggregate(aggregate_query)
    before_count = getattr(before_response, "origins_tags")

    async with get_transaction() as transaction:
        await create_test_tags(transaction)

    after_response = await query.aggregate(aggregate_query)
    after_count = getattr(after_response, "origins_tags")
    assert after_count == before_count + 1


async def test_cope_with_multiple_filters():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(
                match=Filter(
                    amino_acids_tags=tags.amino_value,
                    nucleotides_tags=tags.neucleotide_value,
                )
            ),
            Stage(group=GroupStage(id="$origins_tags")),
        ]
    )
    my_result = [result for result in response if result.id == tags.origin_value]
    assert len(my_result) == 1
    assert my_result[0].count == 1


async def test_able_to_group_obsolete_products():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(match=Filter()),
            Stage(group=GroupStage(id="$origins_tags")),
        ],
        True,
    )
    my_result = [result for result in response if result.id == tags.origin_value]
    assert len(my_result) == 1
    assert my_result[0].count == 1


async def test_throw_exception_for_unrecognized_group_field():
    with pytest.raises(ValidationError) as e:
        await query.aggregate(
            [
                Stage(match=Filter()),
                Stage(group=GroupStage(id="$invalid_tag")),
            ],
            True,
        )
    main_error = e.value.errors()[0]
    assert main_error["type"] == "enum"
    assert main_error["loc"][0] == "id"


async def test_group_products_with_a_nutrient_filter():
    async with get_transaction() as transaction:
        tags = await create_test_tags(transaction)

    response = await query.aggregate(
        [
            Stage(
                match=Filter(
                    **{
                        f"{NUTRIENT_TAG}.{tags.nutrient_tag}_100g": Qualify(
                            qualify_gte=0.11
                        )
                    }
                )
            ),
            Stage(group=GroupStage(id="$origins_tags")),
        ]
    )
    my_result = [result for result in response if result.id == tags.origin_value]
    assert len(my_result) == 1
    assert my_result[0].count == 2
