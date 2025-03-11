from pydantic import BaseModel
from query.models.country import Country
from query.models.product import Product


class ScansByCountry(BaseModel):
    product: Product
    country: Country
    year: int
    unique_scans: int