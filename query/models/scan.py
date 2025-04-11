"""Models used by the Scans API"""

import typing
from enum import StrEnum, auto
from typing import Annotated, Dict

from pydantic import BaseModel, Field, RootModel

from query.tables.country import country_codes


class CountryCode(StrEnum):
    """Valid 2-letter country codes"""

    world = auto()


if not typing.TYPE_CHECKING:
    CountryCode = StrEnum("CountryCode", country_codes())


class ScansByCountry(RootModel):
    """Scans by country for a particular year"""

    root: Dict[
        Annotated[CountryCode, Field(description="Two character country code")],
        Annotated[int, Field(examples=[5, 8])],
    ]


class ScanCounts(BaseModel):
    """Overall scan statistics for a year"""

    scans_n: int = Field(examples=[10, 50])
    unique_scans_n: int = Field(examples=[8, 36])
    unique_scans_n_by_country: ScansByCountry


class ScanYears(RootModel):
    """Collection of years over which the product has been scanned"""

    # Note the key should be an int but JSON (and hence OpenAPI) only supports strings for object keys
    root: Dict[
        Annotated[str, Field(description="Year", examples=["2023", "2024"])], ScanCounts
    ]


class ProductScans(RootModel):
    """List of product codes and associated scans by year"""

    root: Dict[Annotated[str, Field(description="Product code")], ScanYears]
