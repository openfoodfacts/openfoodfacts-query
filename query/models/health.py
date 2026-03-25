"""Models used by the health check service"""

from enum import Enum
from typing import Dict

from pydantic import BaseModel


class HealthStatusEnum(str, Enum):
    ok = "ok"
    error = "error"


class HealthItemStatusEnum(str, Enum):
    up = "up"
    down = "down"


class HealthItem(BaseModel):
    status: HealthItemStatusEnum = HealthItemStatusEnum.up
    reason: str | None = None
    """Error information if the item is unhealthy"""
    info: Dict | None = None
    """Additional specific information"""


class Health(BaseModel):
    def add(
        self,
        name: str,
        status: HealthItemStatusEnum,
        reason: str = None,
        info: Dict = None,
    ):
        self.info[name] = HealthItem(status=status, reason=reason, info=info)
        if status != HealthItemStatusEnum.up:
            self.status = HealthStatusEnum.error

    status: HealthStatusEnum = HealthStatusEnum.ok
    """Overall health of the service"""

    info: Dict[str, HealthItem] = dict()
    """Health of individual dependencies"""
