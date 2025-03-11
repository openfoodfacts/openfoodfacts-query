from pydantic import BaseModel


class Product(BaseModel):
    id: int = None
    code: str
    creator: str | None = None
    obsolete: bool | None = False