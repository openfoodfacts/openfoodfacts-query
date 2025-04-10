from query.database import get_transaction
from query.services.event_test import sample_event
from query.tables.product_update_event import create_events
from query.test_helper import random_code


async def test_create_events_should_load_duplicates():
    event = sample_event()
    async with get_transaction() as transaction:
        await create_events(transaction, [event, event])

        result = await transaction.fetch(
            "SELECT * FROM product_update_event WHERE message->>'code' = $1",
            event.payload["code"],
        )
        assert len(result) == 2


async def test_create_events_creates_contributors():
    async with get_transaction() as transaction:
        user1 = random_code()
        user2 = random_code()
        # given an existing contributor record
        await transaction.execute("insert into contributor (code) values ($1)", user1)

        # when events are imported
        await create_events(
            transaction,
            [sample_event({"user_id": user1}), sample_event({"user_id": user2})],
        )

        result = await transaction.fetch(
            "select * from contributor where code in ($1, $2) order by id", user1, user2
        )
        assert len(result) == 2
        assert result[1]["id"] == result[0]["id"] + 1


async def test_create_events_ignores_duplicate_revisions():
    async with get_transaction() as transaction:
        # create some products
        code1 = random_code()
        code2 = random_code()
        owner1 = random_code()
        await transaction.execute(
            "insert into product (code, owners_tags) values ($1, $3), ($2, $3)",
            code1,
            code2,
            owner1,
        )

        # create some messages
        await create_events(
            transaction,
            [
                sample_event(
                    {"code": code1, "user_id": "test", "action": "created", "rev": 1}
                ),
                sample_event(
                    {"code": code1, "user_id": "test", "action": "created", "rev": 2}
                ),
                sample_event(
                    {"code": code1, "user_id": "test", "action": "created", "rev": 2}
                ),  # duplicate
                sample_event(
                    {"code": code2, "user_id": "test", "action": "created", "rev": 1}
                ),
            ],
        )
        results = await transaction.fetch(
            "select * from product_update join product on product.id=product_update.product_id where code in ($1, $2)",
            code1,
            code2,
        )
        assert len([result for result in results if result["code"] == code1]) == 2
        assert len([result for result in results if result["code"] == code2]) == 1


async def test_create_events_appends_events_from_multiple_payloads():
    async with get_transaction() as transaction:
        # create a product
        code1 = random_code()
        await transaction.execute("insert into product (code) values ($1)", code1)
        action1 = random_code()
        # create an existing message
        await create_events(
            transaction,
            [
                sample_event(
                    {"code": code1, "action": action1, "user_id": "test", "rev": 1}
                )
            ],
        )

        # add another event
        await create_events(
            transaction,
            [
                sample_event(
                    {"code": code1, "action": action1, "user_id": "test", "rev": 2}
                )
            ],
        )

        results = await transaction.fetch(
            "select * from product_update join product on product.id=product_update.product_id where code = $1",
            code1,
        )
        assert len(results) == 2
