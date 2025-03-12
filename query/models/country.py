from dataclasses import dataclass


@dataclass
class Country():
    tag: str
    code: str | None = None
    id: int = None
