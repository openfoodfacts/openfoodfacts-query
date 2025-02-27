from typing import Union

import asyncpg
from fastapi import FastAPI
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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
async def health(): 

    try:
        conn = await asyncpg.connect(user=settings.POSTGRES_USER, password=settings.POSTGRES_PASSWORD,
                                 database=settings.POSTGRES_DB, host=settings.POSTGRES_HOST)
        await conn.fetch('SELECT 1 FROM product LIMIT 1')
        await conn.close()
    except Exception as e:
        return {"health": e}
    
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=1000)
        await client.admin.command('ping')
    except Exception as e:
        return {"health": e}
    return {"health": 1}
   

