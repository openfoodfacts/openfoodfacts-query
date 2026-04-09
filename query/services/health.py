"""Provides information on the health of other services that this service depends on"""

import redis.asyncio as redis

from query.services.event import STREAM_NAME
from query.tables.collection_type import FOOD, get_last_updated
from query.tables.settings import get_last_message_id

from ..config import config_settings
from ..database import get_transaction
from ..models.health import Health, HealthItemStatusEnum
from ..mongodb import find_products


async def check_health():
    health = Health()

    try:
        info = {}
        async with get_transaction() as transaction:
            info["last_scheduled_update"] = await get_last_updated(transaction, FOOD)
        health.add("postgres", HealthItemStatusEnum.up, info=info)
    except Exception as e:
        health.add("postgres", HealthItemStatusEnum.down, str(e))

    try:
        async with find_products({"code": "0"}, {"_id": True}) as cursor:
            async for record in cursor:
                pass
        health.add("mongodb", HealthItemStatusEnum.up)
    except Exception as e:
        health.add("mongodb", HealthItemStatusEnum.down, str(e))

    try:
        redis_client = redis.Redis.from_url(config_settings.REDIS_URL)
        redis_info = await redis_client.xinfo_stream(STREAM_NAME)
        info = {"last-generated-id": redis_info["last-generated-id"]}
        try:
            async with get_transaction() as transaction:
                info["last-processed-id"] = await get_last_message_id(transaction)
        except Exception:
            redis_info["last-processed-id"] = "Unknown"

        health.add("redis", HealthItemStatusEnum.up, info=info)
    except Exception as e:
        health.add("redis", HealthItemStatusEnum.down, str(e))

    return health
