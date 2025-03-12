import redis.asyncio as redis
from query.database import database_connection
from query.config import config_settings
from query.models.health import Health, HealthItemStatusEnum
from query.models.query import Filter
from query.mongodb import find_products


async def check_health():
    health = Health()

    try:
        async with database_connection() as conn:
            await conn.fetch("SELECT 1 FROM product LIMIT 1")
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

    # TODO: Should maybe throw and exception here and format with a custom exception handler: https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
    return health
