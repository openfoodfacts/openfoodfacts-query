"""Enums and models relating to product data"""

from enum import Enum


class Source(str, Enum):
    """Where the product data came from"""

    full_load = "full"
    """Product was loaded during a full database load"""

    event = "event"
    """Product was loaded / updated in response to an event"""

    incremental_load = "incremental"
    """Product was refreshed during an incremental load"""
