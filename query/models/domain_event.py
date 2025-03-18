from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class DomainEvent(BaseModel):
    id: str
    type: str
    timestamp: datetime
    payload: Dict
    