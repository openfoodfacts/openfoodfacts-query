"""Models used by the Scans API"""

from typing import Annotated, Dict

from pydantic import BaseModel, Field, RootModel


class ScansByCountry(RootModel):
    """Scans by country for a particular year"""

    root: Dict[
        Annotated[
            str,
            Field(
                description="Two character country code", examples=["fr", "uk", "world"]
            ),
        ],
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
