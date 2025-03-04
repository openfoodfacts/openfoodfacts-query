from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from query.db import Database
from query.config import config_settings
from query.models.health import Health, HealthItemStatusEnum


async def check_health():
    health = Health()

    try:
        async with Database() as conn:
            await conn.fetch("SELECT 1 FROM product LIMIT 1")
        health.add("postgres", HealthItemStatusEnum.up)
    except Exception as e:
        health.add("postgres", HealthItemStatusEnum.down, str(e))

    try:
        client = AsyncIOMotorClient(config_settings.MONGO_URI, serverSelectionTimeoutMS=1000)
        await client.admin.command("ping")
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
