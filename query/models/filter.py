from typing import Dict, Optional
import typing
from pydantic import BaseModel, ConfigDict, Field, create_model
from query.tables.product_tags import tag_tables


class Qualify(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ne: str = Field(alias='$ne')

    
class Filter(BaseModel):
    # and_expression: Annotated[str, Field(alias='$and', default=None)]

    model_config = ConfigDict(extra='allow')

    __pydantic_extra__: Dict[str, str | Qualify] = Field(init=False)

# The type checker can't cope with a dynamic model so skip that here
if not typing.TYPE_CHECKING:
    keys = {key.replace('_', '-'): (Optional[str | Qualify], Field(alias=key, default=None)) for key in tag_tables.keys()}
    keys['model_config'] = (ConfigDict(extra='forbid'))
    Filter = create_model('Filter', __base__ = Filter, **keys)
