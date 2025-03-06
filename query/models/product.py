from pydantic import BaseModel


class Product(BaseModel):
    code: str
    creator: str | None = None
    obsolete: bool | None = False