import typing
from enum import Enum
from typing import Dict, List, Tuple

from pydantic import BaseModel, ConfigDict, Field, create_model

from query.tables.product import product_filter_fields
from query.tables.product_tags import TAG_TABLES


class Qualify(BaseModel, populate_by_name=True, extra="forbid"):
    qualify_ne: str = Field(alias="$ne", default=None)
    qualify_all: List[str] = Field(alias="$all", default=None)
    qualify_in: List[str] | Tuple[None, List[None]] = Field(alias="$in", default=None)
    qualify_nin: List[str] | Tuple[None, List[None]] = Field(alias="$nin", default=None)


class Fragment(BaseModel, extra="allow"):
    pass
    # Could add this for generic IDE validation but VSCode doesn't seem to recognise it
    # __pydantic_extra__: Dict[str, str | Qualify] = Field(init=False)


# The type checker can't cope with a dynamic model so skip that here
if not typing.TYPE_CHECKING:
    keys = {
        key.replace("_", "-"): (str | Qualify, Field(alias=key, default=None))
        for key in (list(TAG_TABLES.keys()) + product_filter_fields())
    }
    keys["model_config"] = ConfigDict(extra="forbid")
    Fragment = create_model("Fragment", __base__=Fragment, **keys)


class Filter(Fragment, populate_by_name=True):
    # $and is only allowed on the root filter
    qualify_and: List[Fragment] | None = Field(alias="$and", default=None)


GroupField = Enum("GroupFields", [("TAG1", "$tag1")])
if not typing.TYPE_CHECKING:
    GroupField = Enum(
        "GroupFields",
        [
            (key.replace("_", "-"), "$" + key)
            for key in (list(TAG_TABLES.keys()) + product_filter_fields())
        ],
    )


class GroupStage(BaseModel, populate_by_name=True, extra="forbid"):
    id: GroupField = Field(alias="_id", default=None)


class Stage(BaseModel, populate_by_name=True, extra="forbid"):
    match: Filter = Field(alias="$match", default=None)
    group: GroupStage = Field(alias="$group", default=None)
    count: int = Field(alias="$count", default=None, multiple_of=1, le=1, ge=1)
    limit: int = Field(alias="$limit", default=None)
    skip: int = Field(alias="$skip", default=None)


class AggregateResult(BaseModel, populate_by_name=True):
    id: str = Field(alias="_id", default=None)
    count: int


class AggregateCountResult(BaseModel, extra="allow"):
    __pydantic_extra__: Dict[str, int]


class SortDirection(int, Enum):
    asc = 1
    desc = -1


class SortColumn(str, Enum):
    popularity = "popularity_key"


class FindQuery(BaseModel):
    filter: Filter
    projection: Dict[str, bool]
    sort: List[Tuple[SortColumn, SortDirection]]
    limit: int = None
    skip: int = None
