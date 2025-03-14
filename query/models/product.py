from dataclasses import dataclass
import datetime
from enum import Enum


class Source(str, Enum):
    full_load = "full"
    event = "event"
    incremental_load = 'incremental'
    

@dataclass
class Product():
    code: str
    process_id: int = 0
    creator: str | None = None
    obsolete: bool | None = False
    source: Source = Source.full_load
    last_processed: datetime = datetime.datetime.now(datetime.timezone.utc)
    revision: int = 0
    id: int = None
