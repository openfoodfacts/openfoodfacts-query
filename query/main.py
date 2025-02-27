from enum import Enum
from typing import Dict, Union

import asyncpg
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    MONGO_URI: str

settings = Settings()

class HealthStatusEnum(str, Enum):
    ok = 'ok'
    error = 'error'

class HealthItemStatusEnum(str, Enum):
    up = 'up'
    down = 'down'

class HealthItem(BaseModel):
    status: HealthItemStatusEnum = HealthItemStatusEnum.up
    reason: str | None = None

class Health(BaseModel):
    def add(self, name: str, status: HealthItemStatusEnum, reason: str = None):
        self.info[name] = HealthItem(status=status, reason=reason)
        if status != HealthItemStatusEnum.up:
            self.status = HealthStatusEnum.error
        
    status: HealthStatusEnum = HealthStatusEnum.ok
    info: Dict[str, HealthItem] = dict()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/health", response_model_exclude_none=True)
async def health() -> Health: 
    health = Health()

    try:
        conn = await asyncpg.connect(user=settings.POSTGRES_USER, password=settings.POSTGRES_PASSWORD,
                                 database=settings.POSTGRES_DB, host=settings.POSTGRES_HOST)
        await conn.fetch('SELECT 1 FROM product LIMIT 1')
        await conn.close()
        health.add('postgres', HealthItemStatusEnum.up)
    except Exception as e:
        health.add('postgres', HealthItemStatusEnum.down, str(e))

    try:
        client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=1000)
        await client.admin.command('ping')
        health.add('mongodb', HealthItemStatusEnum.up)
    except Exception as e:
        health.add('mongodb', HealthItemStatusEnum.down, str(e))

    return health
   

