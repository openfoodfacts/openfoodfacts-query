import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import json
import logging
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

STREAM_NAME = 'product_updates'
async def redis_listener():
    async with redis_client() as redis:
        async with database_connection() as connection:
            last_message_id = await get_last_message_id()
            while True:
                try:
                    response = await redis.xread({STREAM_NAME: last_message_id}, 1000, 5000)
                    # response is an array of tuples of stream name and array of messages
                    if response:
                        await messages_received(response)
                        # Each message is a tuple of the message id followed by a dict that is the payload
                        last_message = response[0][1][-1]
                        await set_last_message_id(connection, last_message[0])

                    # Add a sleep here so that asyncio can drop out when the task is cancelled
                    await asyncio.sleep(0.001)
                except Exception as e:
                    logger.error(repr(e))
                    break


async def messages_received(streams):
    for stream in streams:
        stream_name = stream[0]
        messages = stream[1]
        
        events: List[DomainEvent] = []
        # Reformat the messages and then pass them off to the service
        # All of the product-opener specific code is here, such as converting the diffs to JSON, removing nulls and interpreting the timestamp
        for message in messages:
            id: str = message[0]
            payload: Dict = message[1]
            try:
                timestamp = datetime.fromtimestamp(payload['timestamp'], timezone.utc)
            except:
                try:
                    timestamp = datetime.fromtimestamp(int(id.split('-')[1]), timezone.utc)
                except:
                    timestamp = datetime.now(timezone.utc)

            comment = payload.get('comment')
            if comment != None and '\0' in comment:
                payload['comment'] = comment.replace('\0', '')

            diffs = payload.get('diffs')
            if diffs != None:
                if '\0' in diffs:
                    diffs = diffs.replace('\0', '')
                payload['diffs'] = json.loads(diffs)
                
            events.append(DomainEvent(id=id, timestamp=timestamp,payload=payload, type=stream_name))
            
        await process_events(events)
        
    