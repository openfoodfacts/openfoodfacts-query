"""Provides information on the health of other services that this service depends on"""

import redis.asyncio as redis

from ..config import config_settings
from ..database import get_transaction
from ..models.health import Health, HealthItemStatusEnum
from ..mongodb import find_products


async def check_health():
    health = Health()

    try:
        async with get_transaction() as transaction:
            await transaction.fetch("SELECT 1 FROM product LIMIT 1")
        health.add("postgres", HealthItemStatusEnum.up)
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
        await redis_client.ping()
        health.add("redis", HealthItemStatusEnum.up)
    except Exception as e:
        health.add("redis", HealthItemStatusEnum.down, str(e))

    return health
