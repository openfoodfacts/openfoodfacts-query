import logging
from typing import Dict, List

from fastapi import HTTPException, status
from query.db import Database
from query.models.filter import Filter
from query.tables.product_tags import tag_tables
from query.tables.loaded_tag import get_loaded_tags

logger = logging.getLogger(__name__)

async def count(filter: Filter = None, obsolete = False):
    async with Database() as conn:
        tag_filters = []
        params = []
        if filter:
            loaded_tags = await get_loaded_tags(conn)
            fragments = filter.filter_and or [filter]
            for fragment in fragments:
                for tag, value in fragment.model_dump(exclude_defaults=True, by_alias=True).items():
                    if tag not in loaded_tags:
                        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Tag '{tag}' is not loaded")

                    is_not = False
                    values = [value]
                    if isinstance(value, Dict):
                        if '$ne' in value:
                            is_not = True
                            values = [value['$ne']]
                        elif '$all' in value:
                            values = value['$all']
                        elif '$in' in value:
                            values = [value['$in']]
                        # TODO throw exception if unknown object (although Pydantic may never allow this)

                    for tag_value in values:
                        params.append(tag_value)
                        value_placeholder = f"${len(params)}"
                        if isinstance(tag_value, List):
                            value_placeholder = f"ANY({value_placeholder}::text[])"
                        tag_filters.append( f" AND {'NOT ' if is_not else ''}EXISTS (SELECT * FROM {tag_tables[tag]} WHERE product_id = p.id AND value = {value_placeholder})")
        
        sql = f"SELECT count(*) count FROM product p WHERE {'' if obsolete else 'NOT '}obsolete{''.join(tag_filters)}"
        logger.debug(f"Count: {sql}")
        results = await conn.fetchrow(sql, *params)
        return results['count']
    