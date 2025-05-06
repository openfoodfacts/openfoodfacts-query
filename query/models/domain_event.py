"""API models for domain events, such as product updates"""

from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class DomainEvent(BaseModel):
    """A single domain event"""

    id: str
    """Event identifier. Should be globally unique"""
    type: str
    """The type of event. For Redis this is the stream name"""
    timestamp: datetime
    """When the change that triggered the event took place"""
    payload: Dict
    """Additional information that is specific to the event type"""
