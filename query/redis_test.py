import asyncio
import logging
import math
import time
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from redis.asyncio import Redis, ResponseError, from_url
from testcontainers.redis import RedisContainer

from query.database import get_transaction
from query.redis import (
    STREAM_NAME,
    get_message_timestamp,
    get_retry_interval,
    messages_received,
    redis_client,
    redis_listener,
)
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


async def cancel_task(task: asyncio.Task):
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


async def messages_processed(messages_received_mock: Mock, call_count=1):
    # Have tried a number of ways to wait for messages to be received,
    # such as using a Future, but the sleep seems essential for it to work
    for i in range(10):
        await asyncio.sleep(0.2)
        if messages_received_mock.call_count >= call_count:
            break


@patch("query.redis.get_last_message_id")
@patch("query.redis.set_last_message_id")
@patch("query.redis.messages_received")
async def test_listener_calls_subscriber_function(
    messages_received: Mock, set_id: Mock, get_id: Mock
):
    async with redis_client() as redis:
        # Get the most recent message id so we don't pick up old messages
        get_id.return_value = await get_last_message_id(redis, STREAM_NAME)

        # Add some messages
        product_code = random_code()
        message_id1 = await add_test_message(redis, product_code)
        message_id2 = await add_test_message(redis, random_code())

        # Start the redis listener
        redis_listener_task = asyncio.create_task(redis_listener())

        await messages_processed(messages_received)

        # Settings should be updated with the last message id
        assert set_id.call_args[0][1] == message_id2

        streams = messages_received.call_args[0][1]
        assert len(streams) == 1
        assert streams[0][0] == STREAM_NAME

        messages = streams[0][1]
        assert len(messages) == 2

        # Messages should be in order
        assert messages[0][0] == message_id1
        assert messages[0][1]["code"] == product_code

        await cancel_task(redis_listener_task)


@patch("query.redis.get_last_message_id")
@patch("query.redis.set_last_message_id")
@patch("query.redis.messages_received")
async def test_listener_keeps_track_of_last_message_id(
    messages_received: Mock, set_id: Mock, get_id: Mock
):
    async with redis_client() as redis:
        # Get the most recent message id so we don't pick up old messages
        get_id.return_value = await get_last_message_id(redis, STREAM_NAME)

        # Add a messages
        product_code = random_code()
        await add_test_message(redis, product_code)

        # Start the redis listener
        redis_listener_task = asyncio.create_task(redis_listener())

        await messages_processed(messages_received)
        await cancel_task(redis_listener_task)

        # Settings should only have been called once
        assert set_id.call_count == 1
        # messages_received should only have been called once
        assert messages_received.call_count == 1


def test_retry_interval():
    interval1 = get_retry_interval()
    interval2 = get_retry_interval()
    assert interval2 == interval1 * 2


@patch("query.redis.get_last_message_id")
@patch("query.redis.set_last_message_id")
@patch("query.redis.messages_received")
@patch("query.redis.redis_client")
@patch("query.redis.logger.error")
@patch("query.redis.get_retry_interval")
async def test_listener_retrys_on_error(
    get_retry_interval: Mock,
    error_log: Mock,
    redis_mock: Mock,
    messages_received: Mock,
    set_id: Mock,
    get_id: Mock,
):
    # Create a separate redis container for this test
    redis_container = RedisContainer()

    redis_container.start()
    redis_port = redis_container.get_exposed_port(6379)
    redis_url = f"redis://{redis_container.get_container_host_ip()}:{redis_port}"
    try:
        redis = from_url(redis_url, decode_responses=True)

        # Start from message id 0
        get_id.return_value = "0"

        # Stop our redis instance
        redis_container.stop()

        # Make the redis listener use our stopped instance
        redis_mock.return_value = redis
        try:
            # Set fast retry for test
            get_retry_interval.return_value = 0.1

            # Start the redis listener
            redis_listener_task = asyncio.create_task(redis_listener())

            await messages_processed(messages_received, 0)

            # Error should be logged
            assert not messages_received.called
            assert error_log.called
        finally:
            # Re-start the redis container on the same port
            redis_container.with_bind_ports(6379, redis_port).start()

        # Add a message
        product_code = random_code()
        message_id = await add_test_message(redis, product_code)

        # Wait for retry
        await messages_processed(messages_received, 1)

        assert messages_received.called
        assert set_id.call_args[0][1] == message_id

    finally:
        await cancel_task(redis_listener_task)

        redis_container.stop()


@patch("query.redis.process_events")
async def test_messages_received_strips_nulls(process_events: Mock):
    async with get_transaction() as transaction:
        test_message = {
            "timestamp": 1692032161,
            "code": random_code(),
            "rev": 1,
            "flavor": "off",
            "product_type": "food",
            "user_id": "test_user",
            "action": "updated",
            "comment": "Test \0 after null",
            "diffs": '{"fields":{"change":["categories\0 after null"],"delete":["product_name"]}}',
        }

        await messages_received(
            transaction, [["test-stream", [["test-id", test_message]]]]
        )

        assert process_events.called
        assert process_events.call_args[0][1]
        event = process_events.call_args[0][1][0]
        assert event.id == "test-id"
        assert event.timestamp == datetime.fromtimestamp(
            test_message["timestamp"], timezone.utc
        )
        assert event.payload["comment"] == "Test  after null"
        assert event.payload["diffs"]["fields"]["change"][0] == "categories after null"


@patch("query.redis.process_events")
async def test_copes_with_missing_fields(process_events: Mock):
    async with get_transaction() as transaction:
        test_message = {}

        await messages_received(
            transaction, [["test-stream", [[f"0-1692032161", test_message]]]]
        )

        assert process_events.called
        assert process_events.call_args[0][1]
        event = process_events.call_args[0][1][0]
        assert event.id == "0-1692032161"
        assert event.timestamp == datetime.fromtimestamp(1692032161, timezone.utc)


def test_message_timestamp_returns_a_date_from_a_message_id():
    time_number = math.floor(time.time())
    test_timestamp = get_message_timestamp(f"{time_number}-0", None)
    assert test_timestamp == datetime.fromtimestamp(time_number, timezone.utc)


def test_message_timestamp_returns_the_current_date_for_an_invalid_message_id():
    timestamp = datetime.now(timezone.utc)
    test_timestamp = get_message_timestamp("invalid", None)
    assert test_timestamp >= timestamp


def test_message_timestamp_copes_with_a_null_id():
    timestamp = datetime.now(timezone.utc)
    test_timestamp = get_message_timestamp(None, None)
    assert test_timestamp >= timestamp


def test_message_timestamp_uses_timestamp_if_provided():
    time_number = math.floor(time.time())
    test_timestamp = get_message_timestamp("100-0", {"timestamp": time_number})
    assert test_timestamp == datetime.fromtimestamp(time_number, timezone.utc)
