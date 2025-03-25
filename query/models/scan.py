from typing import Annotated, Dict
from pydantic import BaseModel, Field, RootModel


class ScansByCountry(RootModel):
    root: Dict[Annotated[str, Field(description="Two character country code")], Annotated[int, Field(examples=[5,8])]]
    
class ScanCounts(BaseModel):
      scans_n: int = Field(examples=[10, 50])
      unique_scans_n: int = Field(examples=[8, 36])
      # TODO: Could make the key to this dict a fixed enumeration of 2 character country codes
      unique_scans_n_by_country: ScansByCountry

class ScanYears(RootModel):
    # Note the key should be an int but JSON (and hence OpenAPI) only supports strings for object keys
    root: Dict[Annotated[str, Field(description="Year", examples=["2023","2024"])], ScanCounts]

class ProductScans(RootModel):
    root: Dict[Annotated[str, Field(description="Product code")], ScanYears]
