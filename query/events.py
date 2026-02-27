"""Redis is used to handle asynchronous message exchange between Open Food Facts components"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
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

def get_retry_interval(error_count):
    """Use exponential backoff if we get an error"""
    error_count += 1
    return 2 ** (error_count - 1)

def split_messages(redis_response):
    """Chunk a list of message stream in two equal parts"""
    result = []
    for stream_name, messages in redis_response:
        middle = len(messages) // 2
        result.append([[stream_name, messages[0:middle]]])
        result.append([[stream_name, messages[middle:]]])
    return result

def add_failed_item_to_retry(items_to_retry, item):
    # there must be only one message
    if len(item[1]) > 1:
        logger.error("Expecting a single message in add_failed_item_to_retry, got %d", len(item[1]))
        # continue all the same
    stream_name = item[0]
    msg = item[1][0]
    msg_id = msg[0]
    if (stream_name, msg_id) not in items_to_retry:
        # first time
        error_count = 1
    else:
        error_count = items_to_retry[(stream_name, msg_id)][2] + 1
    items_to_retry[(stream_name, msg_id)] = [item, datetime.now(timezone.utc) + timedelta(seconds=get_retry_interval(error_count)), error_count]
    return (stream_name, msg_id)

def clear_items_to_retry(items_to_retry, processed_chunk):
    for stream_name, messages in processed_chunk:
        for msg in messages:
            items_to_retry.pop((stream_name, msg[0]), None)

async def redis_listener():
    """Listen for Redis events on the specified stream and processes any messages received"""
    # dict associating msg_id to (mgs, next_try_time, error_count) 
    items_to_retry = {}
    async with get_transaction() as transaction:
        last_message_id = await get_last_message_id(transaction)

    async with redis_client() as redis:
        redis_error_count = 0
        while True:
            try:
                response = await redis.xread({STREAM_NAME: last_message_id}, 1000, 5000)
                # success resets redis_error_count
                redis_error_count = 0
            except Exception as e:
                response = None
                redis_error_count += 1
                retry_in = get_retry_interval(redis_error_count)
                logger.error(
                    f"Error getting messages. Retrying {retry_in} s. {repr(e)}"
                )
                # Exponential back-off indefinitely, Listener will be completely stopped by scheduled import every 24 hours
                await asyncio.sleep(retry_in)

            # response is an array of tuples of stream name and array of messages
            if response:
                # we might also have items to retry, and we will do them one by one
                to_retry = [[item] for item, retry_time, _ in items_to_retry.values() if retry_time < datetime.now()]
                # retry will be done one by one to avoid problems appart
                to_process = [response] + to_retry
                while to_process:
                    chunk = to_process.pop(0)
                    try:
                        async with get_transaction() as transaction:
                            await messages_received(transaction, chunk)
                            # Each message is a tuple of the message id followed by a dict that is the payload
                            last_message_id = chunk[0][1][-1][0]
                            await set_last_message_id(transaction, last_message_id)
                        # if sucessful remove msgs from items_to_retry
                        clear_items_to_retry(items_to_retry, chunk)
                    except Exception as e:
                        # on error try to chunk problematic chunk down
                        if len(chunk[0][1]) > 1:
                            logger.exception(
                                f"Error processing {len(chunk[0][1])} messages. Splitting and retrying."
                            )
                            to_process[0:0] = split_messages(chunk)
                        else:
                            # we got a problematic item, let's try again later
                            stream_name, msg_id = add_failed_item_to_retry(items_to_retry, chunk[0])
                            _error_count = items_to_retry[(stream_name, msg_id)][2]
                            logger.exception(
                                f"Error processing message {stream_name}, {msg_id} for the {_error_count} time."
                            )


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

                # remove ip if there is one
                payload.pop("ip", None)

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
