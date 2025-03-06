from typing import Dict

from fastapi import HTTPException, status
from query.db import Database
from query.models.filter import Filter
from query.tables.product_tags import tag_tables
from query.tables.loaded_tag import get_loaded_tags

async def count(filter: Filter):
    async with Database() as conn:
        loaded_tags = await get_loaded_tags(conn)
        tag_filter = ''
        params = []
        for tag, value in filter.model_dump(exclude_defaults=True, by_alias=True).items():
            if tag not in loaded_tags:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Tag '{tag}' is not loaded")

            is_not = False
            if isinstance(value, Dict):
                is_not = True
                value = value['$ne'] 

            params.append(value)
            tag_filter += f' AND {"NOT " if is_not else ""}EXISTS (SELECT * FROM {tag_tables[tag]} WHERE product_id = p.id AND value = ${len(params)})'
        
        results = await conn.fetchrow(f'SELECT count(*) count FROM product p WHERE NOT obsolete{tag_filter}', *params)
        return results['count']