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


class Health(BaseModel):
    def add(self, name: str, status: HealthItemStatusEnum, reason: str = None):
        self.info[name] = HealthItem(status=status, reason=reason)
        if status != HealthItemStatusEnum.up:
            self.status = HealthStatusEnum.error

    status: HealthStatusEnum = HealthStatusEnum.ok
    info: Dict[str, HealthItem] = dict()
