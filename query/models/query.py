"""Models used by the aggregate, count and find APIs"""

import typing
from enum import Enum
from typing import Annotated, Any, Dict, List, Tuple

from pydantic import BaseModel, Field, create_model

from ..tables.product import product_fields

NoValues = Annotated[
    Tuple[None, List[None]],
    Field(description="Special value used to match a null or empty array"),
]

ScalarValue = str | int | float


class Qualify(BaseModel, validate_by_name=True, extra="forbid"):
    """Qualifiers are special words used as keys in mongo queries
    that roughly correspond to operators"""

    # Because of the `$`, we enable validation using the name when we populate models in code
    qualify_ne: ScalarValue = Field(None, alias="$ne", description="Not equal to")
    qualify_lt: ScalarValue = Field(None, alias="$lt", description="Less than")
    qualify_lte: ScalarValue = Field(
        None, alias="$lte", description="Less than or equal"
    )
    qualify_gt: ScalarValue = Field(None, alias="$gt", description="Greater than")
    qualify_gte: ScalarValue = Field(
        None, alias="$gte", description="Greater than or equal"
    )
    qualify_all: List[ScalarValue] = Field(
        None,
        alias="$all",
        description="All of the listed values must appear in the referenced tag",
    )
    qualify_in: List[ScalarValue] | NoValues = Field(
        None, alias="$in", description="Value matches at least one of the items listed"
    )
    qualify_nin: List[ScalarValue] | NoValues = Field(
        None, alias="$nin", description="None of the value are in the items listed"
    )


class Fragment(BaseModel, extra="allow"):
    """Fragment of a query"""

    # the real class is dynamically generated below
    __pydantic_extra__: Dict[str, ScalarValue | Qualify]


# The type checker can't cope with a dynamic model so skip that here
if not typing.TYPE_CHECKING:
    # This provides the full list of allowed fields that can be qualified
    keys = {
        key.replace("_", "-"): (ScalarValue | Qualify, Field(alias=key, default=None))
        for key in product_fields()
    }
    Fragment = create_model("Fragment", __base__=Fragment, **keys)


class Filter(Fragment, populate_by_name=True):
    """The filter to be applied to a query. Follows the MongoDB general structure"""

    # $and is only allowed on the root filter
    qualify_and: List[Fragment] | None = Field(
        None,
        alias="$and",
        description="This is only needed if you need to apply multiple criteria to the same field",
    )


GroupField = Enum("GroupFields", [("TAG1", "$tag1")])
if not typing.TYPE_CHECKING:
    # Re-define the fields at runtime to just include allowed values
    GroupField = Enum(
        "GroupFields",
        [(key.replace("_", "-"), "$" + key) for key in product_fields()],
    )


class GroupStage(BaseModel, populate_by_name=True):
    """The field to group by in an aggregation query"""

    id: GroupField = Field(
        None, alias="_id", description="The field name to group by, prefixed with '$'"
    )


LIMIT_DESCRIPTION = "Maximum number of results to return"
SKIP_DESCRIPTION = "Skip records when paginating results"


class Stage(BaseModel, populate_by_name=True):
    """This emulates the different options available in a MongoDB aggregation pipeline. Note that only a limited syntax is supported"""

    match: Filter = Field(None, alias="$match")
    group: GroupStage = Field(None, alias="$group")
    count: Any = Field(
        None,
        alias="$count",
        examples=[1],
        description="Whether to just count the number of groups (like count distinct)",
    )
    limit: int = Field(None, alias="$limit", description=LIMIT_DESCRIPTION, gt=0)
    skip: int = Field(None, alias="$skip", description=SKIP_DESCRIPTION, ge=0)


class AggregateResult(BaseModel, populate_by_name=True):
    """The number of products for each group field"""

    id: str = Field(alias="_id", default=None)
    count: int


class AggregateCountResult(BaseModel, extra="allow"):
    """The number of group values (count distinct)"""

    __pydantic_extra__: Dict[str, int]


class SortDirection(int, Enum):
    """1=ascending, -1=descending"""

    asc = 1
    desc = -1


class SortColumn(str, Enum):
    """The field to sort by"""

    created_t = "created_t"
    last_modified_t = "last_modified_t"
    scans_n = "scans_n"
    unique_scans_n = "unique_scans_n"
    product_name = "product_name"
    completeness = "completeness"
    popularity = "popularity_key"
    nutriscore_score = "nutriscore_score"
    nutriscore_score_opposite = "nutriscore_score_opposite"
    environmental_score_score = "environmental_score_score"


class FindQuery(BaseModel):
    filter: Filter
    projection: Annotated[
        Dict[str, bool], Field(None, description="Fields that should be returned")
    ]
    sort: Annotated[
        List[Tuple[SortColumn, SortDirection]],
        Field(
            None,
            description="How the data should be sorted. Note sorting by a single field is currently supported",
        ),
    ]
    limit: int = Field(None, description=LIMIT_DESCRIPTION, gt=0)
    skip: int = Field(None, description=SKIP_DESCRIPTION, ge=0)
