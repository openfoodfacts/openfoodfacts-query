from typing import Dict
from pydantic import BaseModel, Field


class ScanCounts(BaseModel):
      scans_n: int
      unique_scans_n: int
      # TODO: Could make the key to this dict a fixed enumeration of 2 character country codes
      unique_scans_n_by_country: Dict[str, int]

   
