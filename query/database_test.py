from datetime import datetime, timezone

import pytest
from asyncpg import PostgresError

from .database import create_record, get_rows_affected, get_transaction, strip_nuls
from .test_helper import random_code


async def test_rows_affected_returned_correctly():
    async with get_transaction() as transaction:
        await transaction.execute(
            "CREATE TEMP TABLE product_temp (id int PRIMARY KEY, last_updated timestamptz, data jsonb)"
        )
        result = await transaction.execute(
            "INSERT INTO product_temp (last_updated, id, data) VALUES ($1,$2,$3),($1,$4,$5),($1,$6,$7)",
            datetime(2023, 1, 1, tzinfo=timezone.utc),
            1,
            {"a": 1},
            2,
            {"b": 2},
            3,
            {"c": 3},
        )

        assert get_rows_affected(result) == 3

        result = await transaction.execute(
            "UPDATE product_temp SET data = $1 WHERE id < $2", {"d": 4}, 3
        )
        assert get_rows_affected(result) == 2

        result = await transaction.execute("DELETE FROM product_temp WHERE id < $1", 3)
        assert get_rows_affected(result) == 2


async def test_create_record():
    async with get_transaction() as transaction:
        await transaction.execute(
            "CREATE TEMP TABLE product_temp (id int PRIMARY KEY, last_updated timestamptz, data jsonb)"
        )
        record = await create_record(transaction, "product_temp", id=1, data={"x": 6})
        assert record["id"] == 1
        assert record["data"] == {"x": 6}
        assert record["last_updated"] == None


async def test_transaction_error_closes_connection():
    id = random_code()
    with pytest.raises(PostgresError):
        async with get_transaction() as transaction:
            # Valid SQL
            await transaction.execute("UPDATE settings SET last_message_id = $1", id)

            # Invalid SQL, should cause rollback
            await transaction.execute("UPDATE settings SET invalid_column = $1", id)

    assert transaction.is_closed()

    async with get_transaction() as transaction:
        fetched_id = await transaction.fetchval("SELECT last_message_id FROM settings")
        # Verify the transaction was rolled back
        assert fetched_id != str(id)


def test_strip_nuls_copes_with_dict_values():
    test_dict = {"test": "\x001"}
    strip_nuls(test_dict, "test")
    assert test_dict == {"test": "1"}


def test_strip_nuls_copes_with_sub_objects():
    test_dict = {"test": [{"a": "\x001"}]}
    strip_nuls(test_dict, "test")
    assert test_dict == {"test": [{"a": "1"}]}
