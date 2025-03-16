from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from asyncpg import Record


class Source(str, Enum):
    full_load = "full"
    event = "event"
    incremental_load = 'incremental'
    

@dataclass
class Product:
    code: str
    process_id: int = 0
    creator: str | None = None
    obsolete: bool | None = False
    source: Source = Source.full_load
    last_processed: datetime = datetime.now(timezone.utc)
    last_updated: datetime = datetime.now(timezone.utc)
    name: str = None
    owners_tags: str = None
    revision: int = 0
    ingredients_count: int = None
    ingredients_without_ciqual_codes_count: int = None
    id: int = None
