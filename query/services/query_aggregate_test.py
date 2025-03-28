import pytest
from pydantic import ValidationError

from query.database import database_connection
from query.models.query import Filter, GroupStage, Qualify, Stage
from query.services import query
from query.services.query_count_test import create_test_tags


async def test_group_products_with_a_tag():
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
        response = await query.aggregate(
            [Stage(match=Filter()), Stage(group=GroupStage(id="$origins_tags"))]
        )
        my_result = [result for result in response if result.id == tags.origin_value]
        assert len(my_result) == 1
        assert my_result[0].count == 3


async def test_filter_products_when_grouping():
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
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
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
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
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
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
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
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
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
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
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
        response = await query.aggregate(
            [
                Stage(
                    match=Filter(amino_acids_tags=Qualify(qualify_ne=tags.amino_value))
                ),
                Stage(group=GroupStage(id="$origins_tags")),
            ]
        )
        my_result = [result for result in response if result.id == tags.origin_value]
        assert len(my_result) == 1
        assert my_result[0].count == 1


async def test_able_to_just_count():
    async with database_connection() as connection:
        await create_test_tags(connection)
        aggregate_query = [
            Stage(match=Filter()),
            Stage(group=GroupStage(id="$origins_tags")),
            Stage(count=1),
        ]
        before_response = await query.aggregate(aggregate_query)
        before_count = getattr(before_response, "origins_tags")

        await create_test_tags(connection)
        after_response = await query.aggregate(aggregate_query)
        after_count = getattr(after_response, "origins_tags")
        assert after_count == before_count + 1


async def test_cope_with_multiple_filters():
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
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
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
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
