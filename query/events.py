"""Redis is used to handle asynchronous message exchange between Open Food Facts components"""

import asyncio
import hmac
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, List

import redis.asyncio as redis

from .config import config_settings
from .database import get_transaction, strip_nuls
from .models.domain_event import DomainEvent
from .services.event import STREAM_NAME, process_events
from .tables.settings import (
    apply_pre_migration_message_id,
    get_last_message_id,
    set_last_message_id,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def redis_client() -> AsyncGenerator[redis.Redis, Any]:
    """Creates a connection to Redis"""
    client = redis.from_url(config_settings.REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()


error_count = 0


def get_retry_interval():
    """Use exponential backoff if we get an error"""
    global error_count
    error_count += 1
    return 2 ** (error_count - 1)


async def redis_listener():
    """Listen for Redis events on the specified stream and processes any messages received"""
    global error_count
    error_count = 0
    async with get_transaction() as transaction:
        last_message_id = await get_last_message_id(transaction)

    async with redis_client() as redis:
        while True:
            try:
                response = await redis.xread({STREAM_NAME: last_message_id}, 1000, 5000)
                # response is an array of tuples of stream name and array of messages
                if response:
                    async with get_transaction() as transaction:
                        await messages_received(transaction, response)
                        # Each message is a tuple of the message id followed by a dict that is the payload
                        last_message_id = response[0][1][-1][0]
                        await set_last_message_id(transaction, last_message_id)

                # Reset error count on success
                error_count = 0

            except Exception as e:
                retry_in = get_retry_interval()
                logger.error(
                    f"Error processing messages. Retrying {retry_in} s. {repr(e)}"
                )
                # Exponential back-off indefinitely, Listener will be completely stopped by scheduled import every 24 hours
                await asyncio.sleep(retry_in)


redis_listener_task = None


def start_redis_listener():
    """Starts the redis listener and keeps a handle on the task so it can be paused during scheduled imports"""
    global redis_listener_task
    redis_listener_task = asyncio.create_task(redis_listener())


async def stop_redis_listener():
    """Stops the redis listener. May take a few seconds if we are waiting for messages from Redis"""
    global redis_listener_task
    if redis_listener_task and not redis_listener_task.done():
        redis_listener_task.cancel()
        try:
            await redis_listener_task
        except asyncio.CancelledError:
            logger.debug("Redis listener cancelled successfully")


# Note we keep a global varible here so we can pause and result the listener during imports
@asynccontextmanager
async def redis_lifespan():
    """Lifespan handler for starting and stopping Redis with FastAPI"""
    try:
        # Reset last_message_id to before any data migrations
        await apply_pre_migration_message_id()
        start_redis_listener()
        yield
    finally:
        await stop_redis_listener()


async def messages_received(transaction, streams):
    """Converts a list of messages in one or more streams into domain events for onward processing"""
    for stream in streams:
        stream_name = stream[0]
        messages = stream[1]

        events: List[DomainEvent] = []
        # Reformat the messages and then pass them off to the service
        # All of the product-opener specific code is here, such as converting the diffs to JSON, removing nulls and interpreting the timestamp
        for message in messages:
            try:
                id: str = message[0]
                payload: Dict = message[1]
                timestamp = get_message_timestamp(id, payload)

                strip_nuls(payload, f"Redis event id {id}")
                if "diffs" in payload:
                    payload["diffs"] = json.loads(payload["diffs"])

                # anonymize ip
                if payload.get("ip"):
                    payload["ip"] = hmac.digest(
                        config_settings.APP_SECRET_KEY,
                        str(payload["ip"]).encode("utf-8"),
                        "sha256",
                    ).hex()



                events.append(
                    DomainEvent(
                        id=id, timestamp=timestamp, payload=payload, type=stream_name
                    )
                )
            except Exception as e:
                # Catch individual errors per message so that one message doesn't spoil the batch
                logger.error(f"{repr(e)} for message: {repr(message)}")

        if events:
            await process_events(transaction, events)


def get_message_timestamp(id, payload):
    """Determine the time that the domain event took place"""
    try:
        # Use the timestamp property on the message payload if it is provided
        timestamp = datetime.fromtimestamp(payload["timestamp"], timezone.utc)
    except:
        try:
            # Otherwise attempt extract the timestamp from the message id
            timestamp = datetime.fromtimestamp(int(id.split("-")[0]), timezone.utc)
        except:
            # If all else fails use the current time
            timestamp = datetime.now(timezone.utc)

    return timestamp
