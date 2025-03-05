from typing import Dict
from query.db import Database
from query.models.filter import Filter
from query.tables.product_tags import tag_tables

async def count(filter: Filter):
    tag_filter = ''
    params = []
    for tag, value in filter.model_dump(exclude_defaults=True, by_alias=True).items():
        is_not = False
        if isinstance(value, Dict):
           is_not = True
           value = value['$ne'] 

        params.append(value)
        tag_filter += f' AND {"NOT " if is_not else ""}EXISTS (SELECT * FROM {tag_tables[tag]} WHERE product_id = p.id AND value = ${len(params)})'
        
    async with Database() as conn:
        results = await conn.fetchrow(f'SELECT count(*) count FROM product p WHERE NOT obsolete{tag_filter}', *params)
        return results['count']