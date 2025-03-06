from typing import Dict, List, Optional
import typing
from pydantic import BaseModel, ConfigDict, Field, create_model
from query.tables.product_tags import tag_tables


class Filter(BaseModel):
    # and_expression: Annotated[str, Field(alias='$and', default=None)]

    model_config = ConfigDict(extra="allow")

    # Could add this for generic IDE validation but VSCode doesn't seem to recognise it
    # __pydantic_extra__: Dict[str, str | Qualify] = Field(init=False)


class Qualify(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    ne: str | None = Field(alias="$ne", default=None)
    all: List[str] | None = Field(alias="$all", default=None)


# The type checker can't cope with a dynamic model so skip that here
if not typing.TYPE_CHECKING:
    keys = {
        key.replace("_", "-"): (Optional[str | Qualify], Field(alias=key, default=None))
        for key in tag_tables.keys()
    }
    keys["model_config"] = ConfigDict(extra="forbid")
    Filter = create_model("Filter", __base__=Filter, **keys)
