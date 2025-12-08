import math
import time
from unittest.mock import Mock, patch

from ..database import get_transaction
from ..events import STREAM_NAME
from ..models.domain_event import DomainEvent
from ..models.product import Source
from ..services.event import import_events, process_events
from ..test_helper import random_code
from . import event

message_index = 0


def sample_event(payload={}):
    global message_index
    timestamp = math.floor(time.time())
    message_id = f"{timestamp}-{message_index}"
    message_index += 1
    if "code" not in payload:
        payload["code"] = random_code()
    return DomainEvent(
        id=message_id, timestamp=timestamp, type=STREAM_NAME, payload=payload
    )


@patch.object(event, "import_with_filter")
async def test_process_events_calls_import_with_filter(import_with_filter: Mock):
    async with get_transaction() as transaction:
        event = sample_event({"product_type": "food", "rev": "1"})
        code1 = event.payload["code"]
        await process_events(transaction, [event])

        assert import_with_filter.called
        import_args = import_with_filter.call_args[0]
        assert import_args[1] == {"code": {"$in": [code1]}}
        assert import_args[2] == Source.event

        # Update events are created
        events = await transaction.fetch(
            "SELECT * FROM product_update_event WHERE message->>'code' = $1", code1
        )

        assert len(events) == 1
        assert events[0]["message_id"] == event.id

        # product_update is not created as we have no contributor or action
        updates = await transaction.fetch(
            "SELECT * FROM product_update WHERE event_id = $1", events[0]["id"]
        )
        assert len(updates) == 0


@patch.object(event, "import_with_filter")
async def test_process_events_not_include_non_food_products_in_call_to_import_with_filter(
    import_with_filter: Mock,
):
    async with get_transaction() as transaction:
        food_event = sample_event({"product_type": "food", "rev": "1"})
        food_code = food_event.payload["code"]
        beauty_event = sample_event({"product_type": "beauty", "rev": "1"})
        beauty_code = beauty_event.payload["code"]
        await process_events(transaction, [food_event, beauty_event])

        # Update events are created for all product types
        events = await transaction.fetch(
            "SELECT * FROM product_update_event WHERE message->>'code' in ($1, $2)",
            food_code,
            beauty_code,
        )
        assert len(events) == 2

        # Import only called for the food product
        assert import_with_filter.called
        import_args = import_with_filter.call_args[0]
        assert import_args[1] == {"code": {"$in": [food_code]}}


@patch.object(event, "import_with_filter")
async def test_process_events_does_not_import_with_filter_at_all_if_no_food_products(
    import_with_filter: Mock,
):
    async with get_transaction() as transaction:
        beauty_event = sample_event({"product_type": "beauty", "rev": "1"})
        await process_events(transaction, [beauty_event])

        # Import is not called
        assert not import_with_filter.called


@patch.object(event, "create_events")
async def test_import_events(create_events: Mock):
    product_code = random_code()
    test_message1 = {
        "timestamp": math.floor(time.time()),
        "code": product_code,
        "rev": 1,
        "product_type": "food",
    }
    test_message2 = {
        "timestamp": math.floor(time.time()),
        "code": product_code,
        "rev": 2,
        "product_type": "food",
    }

    await import_events([test_message1, test_message2])

    assert create_events.called
    assert len(create_events.call_args[0][1]) == 2
