from pydantic import BaseModel


class Country(BaseModel):
    id: int = None
    tag: str
    code: str | None = None
