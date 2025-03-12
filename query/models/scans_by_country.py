from dataclasses import dataclass
from query.models.country import Country
from query.models.product import Product


@dataclass
class ScansByCountry():
    product: Product
    country: Country
    year: int
    unique_scans: int