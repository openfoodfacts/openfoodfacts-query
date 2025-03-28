from enum import Enum


class Source(str, Enum):
    full_load = "full"
    event = "event"
    incremental_load = "incremental"
