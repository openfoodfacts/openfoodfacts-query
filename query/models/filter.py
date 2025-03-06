from typing import Dict, List, Optional, Tuple
import typing
from pydantic import BaseModel, ConfigDict, Field, create_model
from query.tables.product_tags import tag_tables
from query.tables.product import product_filter_fields


class Qualify(BaseModel, populate_by_name=True, extra="forbid"):
    qualify_ne: str | None = Field(alias="$ne", default=None)
    qualify_all: List[str] | None = Field(alias="$all", default=None)
    qualify_in: List[str] | Tuple[None, List[None]] | None = Field(alias="$in", default=None)
    qualify_nin: List[str] | Tuple[None, List[None]] | None = Field(alias="$nin", default=None)


class Fragment(BaseModel, extra="allow"):
    pass
    # Could add this for generic IDE validation but VSCode doesn't seem to recognise it
    # __pydantic_extra__: Dict[str, str | Qualify] = Field(init=False)


# The type checker can't cope with a dynamic model so skip that here
if not typing.TYPE_CHECKING:
    keys = {
        key.replace("_", "-"): (Optional[str | Qualify], Field(alias=key, default=None))
        for key in (list(tag_tables.keys()) + list(product_filter_fields.keys()))
    }
    keys["model_config"] = ConfigDict(extra="forbid")
    Fragment = create_model("Fragment", __base__=Fragment, **keys)


class Filter(Fragment, populate_by_name=True):
    # $and is only allowed on the root filter
    qualify_and: List[Fragment] | None = Field(alias="$and", default=None)
