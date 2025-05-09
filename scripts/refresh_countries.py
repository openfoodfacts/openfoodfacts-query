"""Refreshes the countries.json file from the currently published Open Food Facts taxonomy"""

import json
import requests


res = requests.get("https://static.openfoodfacts.org/data/taxonomies/countries.json")
response = res.json()
with open("query/assets/countries.json", "w", encoding="utf-8") as f:
    json.dump(response, f, sort_keys=True, ensure_ascii=False, indent=2)
