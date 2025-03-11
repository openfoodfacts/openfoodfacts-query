import logging
from typing import Dict, List

from fastapi import HTTPException, status
from query.database import database_connection
from query.models.query import AggregateCountResult, AggregateResult, Filter, GroupStage, Stage
from query.tables.product import product_filter_fields
from query.tables.product_tags import tag_tables
from query.tables.loaded_tag import get_loaded_tags

logger = logging.getLogger(__name__)


async def count(filter: Filter = None, obsolete=False):
    async with database_connection() as conn:
        sql_fragments = []
        params = []
        loaded_tags = await get_loaded_tags(conn)
        if filter:
            append_sql_fragments(filter, loaded_tags, "id", params, sql_fragments)

        sql = f"SELECT count(*) count FROM product p WHERE {'' if obsolete else 'NOT '}obsolete{''.join(sql_fragments)}"
        logger.debug(f"Count: SQL:  {sql}")
        logger.debug(f"Count: Args: {repr(params)}")
        results = await conn.fetchrow(sql, *params)
        return results["count"]


async def aggregate(stages: List[Stage], obsolete = False):
    async with database_connection() as conn:
        sql_fragments = []
        params = []
        loaded_tags = await get_loaded_tags(conn)
        group = [stage.group for stage in stages if stage.group][0]
        filter = [stage.match for stage in stages if stage.match][0]
        is_count = [stage.count for stage in stages if stage.count]
        tag = group.id.value[1:]
        is_product_filter = tag in product_filter_fields.keys()

        table_name = "product" if is_product_filter else tag_tables[tag]
        column_name = product_filter_fields[tag] if is_product_filter else "value"
        if filter:
            append_sql_fragments(
                filter,
                loaded_tags,
                "id" if is_product_filter else "product_id",
                params,
                sql_fragments,
            )
        if is_count:
            sql = f"SELECT count(*) count FROM (SELECT DISTINCT {column_name} FROM {table_name} p WHERE {column_name} IS NOT NULL AND {'' if obsolete else 'NOT '}obsolete{''.join(sql_fragments)})"
        else:
            sql = f"SELECT {column_name} id, count(*) count FROM {table_name} p WHERE {column_name} IS NOT NULL AND {'' if obsolete else 'NOT '}obsolete{''.join(sql_fragments)} GROUP BY {column_name} ORDER BY 2 DESC"
        logger.debug(f"Aggregate: SQL:  {sql}")
        logger.debug(f"Aggregate: Args: {repr(params)}")
        results = await conn.fetch(sql, *params)
        if is_count:
            result = AggregateCountResult()
            setattr(result, tag, results[0]['count'])
            return result
        else:
            return [AggregateResult(id=row["id"], count=row["count"]) for row in results]


def append_sql_fragments(
    filter: Filter, loaded_tags, parent_id_column, params, sql_fragments
):
    fragments = filter.qualify_and or [filter]
    for fragment in fragments:
        for tag, value in fragment.model_dump(
            exclude_defaults=True, by_alias=True
        ).items():
            is_product_filter = tag in product_filter_fields.keys()
            if not is_product_filter and tag not in loaded_tags:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY, f"Tag '{tag}' is not loaded"
                )

            is_not = False
            values = [value]
            if isinstance(value, Dict):
                if "$ne" in value:
                    is_not = True
                    values = [value["$ne"]]
                elif "$all" in value:
                    values = value["$all"]
                elif "$in" in value:
                    in_list = value["$in"]
                    # MongoDB does a not exist with $in: [null, []]
                    if in_list[0] == None:
                        in_list = None
                        is_not = True
                    values = [in_list]
                elif "$nin" in value:
                    in_list = value["$nin"]
                    is_not = True
                    # MongoDB does an exists with $nin: [null, []]
                    if in_list[0] == None:
                        in_list = None
                        is_not = False
                    values = [in_list]
                # TODO throw exception if unknown object (although Pydantic may never allow this)

            for tag_value in values:
                where_expression = ""
                field = product_filter_fields[tag] if is_product_filter else "value"
                if tag_value != None:
                    params.append(tag_value)
                    if isinstance(tag_value, List):
                        where_expression = (
                            f" AND {field} = ANY(${len(params)}::text[])"
                        )
                    else:
                        where_expression = f" AND {field} = ${len(params)}"

                if is_product_filter:
                    if tag_value == None:
                        where_expression = f" AND {field} IS {'' if is_not else 'NOT '}NULL"
                    else:
                        if is_not:
                            where_expression = f" AND ({field} IS NULL OR {where_expression.replace(' AND ', ' NOT ')})"
                    # If parent is the product table then we can just add the where clause. Otherwise need an EXISTS
                    if parent_id_column == "id":
                        sql_fragments.append(where_expression)
                    else:
                        sql_fragments.append(f" AND EXISTS (SELECT * FROM product WHERE id = p.product_id{where_expression})")
                        
                else:
                    sql_fragments.append(
                        f" AND {'NOT ' if is_not else ''}EXISTS (SELECT * FROM {tag_tables[tag]} WHERE product_id = p.{parent_id_column}{where_expression})"
                    )
