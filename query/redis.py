import asyncio
from contextlib import asynccontextmanager
import logging
from typing import Any, AsyncGenerator
import redis.asyncio as redis

from query.config import config_settings
from query.database import database_connection
from query.tables.settings import get_last_message_id, set_last_message_id

logger = logging.getLogger(__name__)

@asynccontextmanager
async def redis_client() -> AsyncGenerator[redis.Redis, Any]:
    client = redis.from_url(config_settings.REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()

STREAM_NAME = 'product_updates'
async def redis_listener():
    async with redis_client() as redis:
        async with database_connection() as connection:
            last_message_id = await get_last_message_id()
            while True:
                try:
                    response = await redis.xread({STREAM_NAME: last_message_id}, 1000, 5000)
                    # response is an array of tuples of key and messages
                    if response:
                        messages = response[0][1]
                        await messages_received(messages)
                        # Each message is a tupe of the message id followed by ta dict that is the message
                        last_message = messages[-1]
                        await set_last_message_id(connection, last_message[0])

                    # Add a sleep here so that asyncio can drop out when the task is cancelled
                    await asyncio.sleep(0.001)
                except Exception as e:
                    logger.error(repr(e))
                    break


async def messages_received(messages):
    pass