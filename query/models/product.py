from dataclasses import dataclass


@dataclass
class Product():
    code: str
    creator: str | None = None
    obsolete: bool | None = False
    id: int = None
