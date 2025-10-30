"""Routines that support the query services like count, aggregate and find"""

import logging
from typing import Dict, List

from asyncpg import Connection
from fastapi import HTTPException, status

from query.tables.product_nutrient import NUTRIENT_TAG, NUTRITION_TAG

from ..database import get_transaction
from ..models.query import (
    AggregateCountResult,
    AggregateResult,
    Filter,
    FindQuery,
    SortColumn,
    Stage,
)
from ..mongodb import find_products
from ..tables.country import get_country
from ..tables.loaded_tag import check_tag_is_loaded, get_loaded_tags
from ..tables.product import (
    PRODUCT_FIELD_COLUMNS,
    PRODUCT_FIELD_SCANS_COLUMNS,
    PRODUCT_SCANS_TAG,
    get_product_column_for_field,
)
from ..tables.product_country import PRODUCT_COUNTRY_TAG
from ..tables.product_tags import TAG_TABLES

logger = logging.getLogger(__name__)


async def fetch_and_log(transaction: Connection, sql, *params):
    logger.debug(f"Args: {repr(params)}, SQL: {sql}")
    return await transaction.fetch(sql, *params)


async def count(filter: Filter = None, obsolete=False):
    """Count the number of products that match the specified filter"""
    async with get_transaction() as transaction:
        sql_fragments = []
        params = []
        loaded_tags = await get_loaded_tags(transaction)
        if filter:
            append_sql_fragments(filter, loaded_tags, "id", params, sql_fragments)

        sql = f"""SELECT count(*) count FROM product p
            WHERE {'' if obsolete else 'NOT '}obsolete
            {''.join(sql_fragments)}"""
        return ((await fetch_and_log(transaction, sql, *params)) or [{}])[0].get(
            "count", 0
        )


async def aggregate(stages: List[Stage], obsolete=False):
    """Get aggregate counts based on the stages specified"""
    async with get_transaction() as transaction:
        sql_fragments = []
        params = []
        loaded_tags = await get_loaded_tags(transaction)
        filter = [stage.match for stage in stages if stage.match][0]
        group = [stage.group for stage in stages if stage.group][0]
        # We only currently support grouping by one field
        tag = group.id.value[1:]
        # If a count stage is specified then we just count the distinct number of group field values
        is_count = [stage.count for stage in stages if stage.count]
        product_column_name = get_product_column_for_field(tag, loaded_tags)

        limit = [stage.limit for stage in stages if stage.limit]
        skip = [stage.skip for stage in stages if stage.skip]

        limit_clause = ""
        if limit:
            params.append(limit[0])
            limit_clause += f" LIMIT ${len(params)}"
        if skip:
            params.append(skip[0])
            limit_clause += f" OFFSET ${len(params)}"

        # Determine whether our query is on the product table or one of the tag tables
        table_name = "product" if product_column_name else TAG_TABLES[tag]
        if filter:
            append_sql_fragments(
                filter,
                loaded_tags,
                "id" if product_column_name else "product_id",
                params,
                sql_fragments,
            )
        column_name = product_column_name or "value"
        if is_count:
            sql = f"""SELECT count(*) count FROM 
                (SELECT DISTINCT {column_name} FROM {table_name} p 
                WHERE {column_name} IS NOT NULL AND {'' if obsolete else 'NOT '}obsolete
                {''.join(sql_fragments)})"""
        else:
            sql = f"""SELECT {column_name} id, count(*) count FROM {table_name} p
                WHERE {column_name} IS NOT NULL AND {'' if obsolete else 'NOT '}obsolete
                {''.join(sql_fragments)}
                GROUP BY {column_name} ORDER BY 2 DESC, 1{limit_clause}"""
        results = await fetch_and_log(transaction, sql, *params)
        if is_count:
            result = AggregateCountResult()
            setattr(result, tag, results[0]["count"])
            return result
        else:
            return [
                AggregateResult(id=row["id"], count=row["count"]) for row in results
            ]


async def find(query: FindQuery, obsolete=False):
    """Fetch the product records matching the specified filter, in the requested order,
    returning the fields mentioned in the projection"""
    async with get_transaction() as transaction:
        sort_key = query.sort[0][0] if query.sort and len(query.sort) > 0 else None
        if sort_key and len(query.sort) > 1:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Only a single sort field is supported",
            )

        # Abort for sort on scan field if scans have not yet been fully loaded
        loaded_tags = await get_loaded_tags(transaction)
        # TODO: Could probably encapsulate this a bit more
        if sort_key == SortColumn.popularity:
            check_tag_is_loaded(PRODUCT_COUNTRY_TAG, loaded_tags)
        elif sort_key in PRODUCT_FIELD_SCANS_COLUMNS.keys():
            check_tag_is_loaded(PRODUCT_SCANS_TAG, loaded_tags)

        if sort_key == SortColumn.popularity:
            # The country we are filtering by determines which scans we use to sort the results
            country_tag = getattr(query.filter, "countries-tags")
            country = (
                await get_country(transaction, country_tag)
                if country_tag
                else await get_country(transaction, "en:world")
            )
            if country_tag:
                delattr(query.filter, "countries-tags")

            params = [country["id"]]
            product_id = "product_id"
        else:
            params = []
            product_id = "id"

        sql_fragments = []
        if query.filter:
            append_sql_fragments(
                query.filter,
                loaded_tags,
                product_id,
                params,
                sql_fragments,
            )
        limit_clause = ""
        if query.limit:
            params.append(query.limit)
            limit_clause += f" LIMIT ${len(params)}"
        if query.skip:
            params.append(query.skip)
            limit_clause += f" OFFSET ${len(params)}"

        if sort_key == SortColumn.popularity:
            # The sub-select gets the list of product ids and applies the limits
            # This was found to be the fastest approach as it allows the inner query to
            # operate on just the small product_country table
            # Note we only support descending sort
            sql = f"""SELECT p.code FROM product p 
                JOIN product_country pc ON pc.product_id = p.id AND pc.country_id = $1
                WHERE p.id IN (SELECT p.product_id
                    FROM product_country p
                    WHERE p.country_id = $1 
                    AND {'' if obsolete else 'NOT '}p.obsolete
                    {''.join(sql_fragments)}
                    ORDER BY p.recent_scans DESC, p.total_scans DESC, p.product_id
                    {limit_clause})
                ORDER BY pc.recent_scans DESC, pc.total_scans DESC, pc.product_id"""
        else:
            # Other sort fields are directly on the product table
            sort_clause = ""
            if sort_key:
                sort_direction = query.sort[0][1]
                if sort_key == SortColumn.nutriscore_score_opposite:
                    # Nutriscore sort should be ascending (low nutriscore is good) but MongoDB shows nulls first
                    # so Product Opener uses a nutriscore_score_opposite descending sort.
                    # PostgreSQL treats NULLs as big so we can simply sort on nutriscore_score, ascending
                    sort_key = SortColumn.nutriscore_score
                    sort_direction = -sort_direction

                sort_clause = f"p.{PRODUCT_FIELD_COLUMNS[sort_key]} {'ASC' if sort_direction == 1 else 'DESC NULLS LAST'},"

            sql = f"""SELECT p.code FROM product p 
                WHERE {'' if obsolete else 'NOT '}p.obsolete
                    {''.join(sql_fragments)}
                    ORDER BY {sort_clause} p.id
                    {limit_clause}"""
        results = await fetch_and_log(transaction, sql, *params)
        product_codes = [result["code"] for result in results]
        logger.debug(f"Find: Codes: {repr(product_codes)}")

        # Make sure we pass the code to MongoDB so that we can match up results
        if query.projection and "code" not in query.projection:
            query.projection["code"] = 1

        if query.projection and len(query.projection.keys()) == 1:
            # Only requesting code so we don't need to go to MongoDB. Could extend this for other fields we store in off-query
            # Nee to convert rows to regular dictionaries to keep Pydantic happy
            return [dict(result) for result in results]
        else:
            mongodb_filter = {"_id": {"$in": product_codes}}
            mongodb_results = [None] * len(product_codes)
            async with find_products(
                mongodb_filter, query.projection, obsolete
            ) as cursor:
                async for result in cursor:
                    code_index = product_codes.index(result["code"])
                    mongodb_results[code_index] = result

            # Eliminate any None's from the result. Note this should only happen if there is a mismatch between off-query and MongoDB
            final_result = [result for result in mongodb_results if result]

            if len(final_result) < len(product_codes):
                missing_product_codes = [
                    code
                    for index, code in enumerate(product_codes)
                    if mongodb_results[index] == None
                ]
                logger.warning(
                    f"Following product codes were not found in MongoDB: {repr(missing_product_codes)}"
                )

            return final_result


def append_sql_fragments(
    filter: Filter, loaded_tags, parent_id_column, params, sql_fragments
):
    """Appends a list of where expressions and corresponding SQL bind variables based on the MongoDB filter
    to the supplied sql_fragments and params parameter respectively.
    loaded_tags is the list of tags that have currently been loaded. Any reference to a non-loaded tag
    will raise an unprocessable entity exception which is caught by Product Opener which would then send the
    query directly to MongoDB instead.
    The parent_id_column determines how inner queries join to the product id of the parent table,
    which is assumed to have an alias of 'p'"""
    # Merge the top level with any $and criteria
    fragments = [filter] + (filter.qualify_and or [])
    for fragment in fragments:
        for tag, value in fragment.model_dump(
            exclude_defaults=True, by_alias=True
        ).items():
            # Skip qualify_and as already merged above
            if tag == "$and":
                continue
            product_column_name = get_product_column_for_field(tag, loaded_tags)
            if not product_column_name:
                check_tag_is_loaded(tag, loaded_tags)

            is_not = False
            values = [value]
            operator = "="
            # Apply any specific MongoDB expression if it isn't a simple match
            if isinstance(value, Dict):
                if "$ne" in value:
                    is_not = True
                    values = [value["$ne"]]
                if "$lt" in value:
                    operator = "<"
                    values = [value["$lt"]]
                if "$gt" in value:
                    operator = ">"
                    values = [value["$gt"]]
                if "$lte" in value:
                    operator = "<="
                    values = [value["$lte"]]
                if "$gte" in value:
                    operator = ">="
                    values = [value["$gte"]]
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
                # Pydantic should catch any disallowed operations

            for tag_value in values:
                where_expression = ""
                column_name = product_column_name or "value"
                if tag_value != None:
                    params.append(tag_value)
                    if isinstance(tag_value, List):
                        where_expression = f" AND {column_name} = ANY(${len(params)})"
                    else:
                        where_expression = (
                            f" AND {column_name} {operator} ${len(params)}"
                        )

                if product_column_name:
                    if tag_value == None:
                        where_expression = (
                            f" AND {column_name} IS {'' if is_not else 'NOT '}NULL"
                        )
                    else:
                        if is_not:
                            where_expression = f" AND ({column_name} IS NULL OR {where_expression.replace(' AND ', ' NOT ')})"
                    # If parent is the product table then we can just add the where clause. Otherwise need an EXISTS
                    if parent_id_column == "id":
                        sql_fragments.append(where_expression)
                    else:
                        sql_fragments.append(
                            f" AND EXISTS (SELECT * FROM product WHERE id = p.product_id{where_expression})"
                        )

                elif tag.startswith(f"{NUTRIENT_TAG}.") or tag.startswith(f"{NUTRITION_TAG}."):
                    # Strip off the _100g for the old format or get the item before the "value" for the new format
                    nutrient_tag = tag.split(".")[1][:-5] if tag.startswith(f"{NUTRIENT_TAG}.") else tag.split(".")[3] 
                    params.append(nutrient_tag)
                    sql_fragments.append(
                        f""" AND {'NOT ' if is_not else ''}EXISTS 
                        (SELECT * FROM product_nutrient 
                        JOIN nutrient ON id = nutrient_id AND tag = ${len(params)}
                        WHERE product_id = p.{parent_id_column}{where_expression})"""
                    )
                else:
                    # If the filter is on a tag table then always do this using an exists
                    sql_fragments.append(
                        f" AND {'NOT ' if is_not else ''}EXISTS (SELECT * FROM {TAG_TABLES[tag]} WHERE product_id = p.{parent_id_column}{where_expression})"
                    )
