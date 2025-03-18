import asyncio
import logging
import math
import time
from unittest.mock import Mock, patch

from redis.asyncio import Redis, ResponseError
from query.redis import STREAM_NAME, redis_client, redis_listener
from query.test_helper import random_code

logger = logging.getLogger(__name__)


async def test_redis_connection():
    async with redis_client() as redis:
        message_id = await add_test_message(redis, random_code())
        await redis.ping()
        last_id = await get_last_message_id(redis, STREAM_NAME)
        assert last_id == message_id

        assert (await get_last_message_id(redis, random_code())) == "0"


async def add_test_message(redis: Redis, product_code):
    return await redis.xadd(
        STREAM_NAME,
        {
            "timestamp": math.floor(time.time()),
            "code": product_code,
            "rev": 1,
            "flavor": "off",
            "product_type": "food",
            "user_id": "test_user",
            "action": "updated",
            "comment": "Test",
            "diffs": '{"fields":{"change":["categories"],"delete":["product_name"]}}',
        },
    )


async def get_last_message_id(redis: Redis, stream):
    try:
        info = await redis.xinfo_stream(stream)
        return info["last-generated-id"]
    except ResponseError:
        return "0"


@patch("query.redis.get_last_message_id")
@patch("query.redis.set_last_message_id")
@patch("query.redis.messages_received")
async def test_listener_calls_subscriber_function(
    messages_received: Mock, set_id: Mock, get_id: Mock
):
    async with redis_client() as redis:
        # Get the most recent message id so we don't pick up old messages
        get_id.return_value = await get_last_message_id(redis, STREAM_NAME)

        # Start the redis listener
        redis_listener_task = asyncio.create_task(redis_listener())

        # Cancel the redis listener as soon as the message is received so we don't have to wait another 5 seconds
        messages_received.side_effect = redis_listener_task.cancel

        # Add a message
        product_code = random_code()
        message_id = await add_test_message(redis, product_code)

        # TODO: Would like to find a better way to wait for other tasks to process...
        await asyncio.sleep(0.1)

        assert messages_received.called
        assert set_id.call_args[0][1] == message_id

        messages = messages_received.call_args[0][0]
        assert len(messages) == 1
        assert messages[0][0] == message_id
        assert messages[0][1]['code'] == product_code
