import logging
from typing import Dict, List

from fastapi import HTTPException, status
from query.db import Database
from query.models.filter import Filter
from query.tables.product import product_filter_fields
from query.tables.product_tags import tag_tables
from query.tables.loaded_tag import get_loaded_tags

logger = logging.getLogger(__name__)

async def count(filter: Filter = None, obsolete = False):
    async with Database() as conn:
        sql_fragments = []
        params = []
        if filter:
            loaded_tags = await get_loaded_tags(conn)
            fragments = filter.qualify_and or [filter]
            for fragment in fragments:
                for tag, value in fragment.model_dump(exclude_defaults=True, by_alias=True).items():
                    is_product_filter = tag in product_filter_fields.keys()
                    if not is_product_filter and tag not in loaded_tags:
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
                            in_list = value['$in']
                            # MongoDB does a not exist with $in: [null, []]
                            if in_list[0] == None:
                                in_list = None
                                is_not = True
                            values = [in_list]
                        elif '$nin' in value:
                            in_list = value['$nin']
                            is_not = True
                            # MongoDB does an exists with $nin: [null, []]
                            if in_list[0] == None:
                                in_list = None
                                is_not = False
                            values = [in_list]
                        # TODO throw exception if unknown object (although Pydantic may never allow this)

                    for tag_value in values:
                        value_placeholder = ""
                        field = product_filter_fields[tag] if is_product_filter else 'value'
                        if tag_value != None:
                            params.append(tag_value)
                            if isinstance(tag_value, List):
                                value_placeholder = f" AND {field} = ANY(${len(params)}::text[])"
                            else:
                                value_placeholder = f" AND {field} = ${len(params)}"

                        if is_product_filter:
                            if tag_value == None:
                                sql_fragments.append( f" AND {field} IS {'' if is_not else 'NOT '}NULL")
                            else:
                                sql_fragments.append( f"{value_placeholder}")
                        else:
                            sql_fragments.append( f" AND {'NOT ' if is_not else ''}EXISTS (SELECT * FROM {tag_tables[tag]} WHERE product_id = p.id{value_placeholder})")
        
        sql = f"SELECT count(*) count FROM product p WHERE {'' if obsolete else 'NOT '}obsolete{''.join(sql_fragments)}"
        logger.debug(f"Count: {sql}")
        results = await conn.fetchrow(sql, *params)
        return results['count']
    