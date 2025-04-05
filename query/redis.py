import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, List

import redis.asyncio as redis

from query.config import config_settings
from query.database import database_connection
from query.models.domain_event import DomainEvent
from query.services.event import process_events
from query.tables.settings import get_last_message_id, set_last_message_id

logger = logging.getLogger(__name__)


@asynccontextmanager
async def redis_client() -> AsyncGenerator[redis.Redis, Any]:
    client = redis.from_url(config_settings.REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()


STREAM_NAME = "product_updates"
error_count = 0


def get_retry_interval():
    global error_count
    error_count += 1
    return 2**error_count


async def redis_listener():
    global error_count
    error_count = 0
    async with redis_client() as redis:
        async with database_connection() as connection:
            last_message_id = await get_last_message_id(connection)
            while True:
                try:
                    response = await redis.xread(
                        {STREAM_NAME: last_message_id}, 1000, 5000
                    )
                    # response is an array of tuples of stream name and array of messages
                    if response:
                        await messages_received(response)
                        # Each message is a tuple of the message id followed by a dict that is the payload
                        last_message_id = response[0][1][-1][0]
                        await set_last_message_id(connection, last_message_id)

                except Exception as e:
                    logger.error(repr(e))
                    # Exponential back-off indefinately, Listener will be completely stopped by scheduled import every 24 hours
                    await asyncio.sleep(get_retry_interval())


redis_listener_task = None


def start_redis_listener():
    global redis_listener_task
    redis_listener_task = asyncio.create_task(redis_listener())


async def stop_redis_listener():
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
    try:
        start_redis_listener()
        yield
    finally:
        await stop_redis_listener()


async def messages_received(streams):
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
                try:
                    timestamp = datetime.fromtimestamp(
                        payload["timestamp"], timezone.utc
                    )
                except:
                    try:
                        timestamp = datetime.fromtimestamp(
                            int(id.split("-")[1]), timezone.utc
                        )
                    except:
                        timestamp = datetime.now(timezone.utc)

                comment = payload.get("comment")
                if comment != None and "\0" in comment:
                    payload["comment"] = comment.replace("\0", "")

                diffs = payload.get("diffs")
                if diffs != None:
                    if "\0" in diffs:
                        diffs = diffs.replace("\0", "")
                    payload["diffs"] = json.loads(diffs)

                events.append(
                    DomainEvent(
                        id=id, timestamp=timestamp, payload=payload, type=stream_name
                    )
                )
            except Exception as e:
                # Catch individual errors per message so that one message doesn't spoil the batch
                logger.error(f"{repr(e)} for message: {repr(message)}")

        if events:
            await process_events(events)


def get_message_timestamp(id, payload):
    try:
        timestamp = datetime.fromtimestamp(payload["timestamp"], timezone.utc)
    except:
        try:
            timestamp = datetime.fromtimestamp(int(id.split("-")[0]), timezone.utc)
        except:
            timestamp = datetime.now(timezone.utc)

    return timestamp
