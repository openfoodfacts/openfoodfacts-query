from typing import List

from fastapi import HTTPException, status

from query.tables.product_nutrient import NUTRIENT_TAG, NUTRITION_TAG
from query.tables.product_tags import TAG_TABLES


async def create_table(transaction):
    await transaction.execute(
        "create table loaded_tag (id text not null, constraint loaded_tag_pkey primary key (id))",
    )


_loaded_tags: List[str] | None = None


async def get_loaded_tags(transaction):
    global _loaded_tags
    if _loaded_tags == None:
        _loaded_tags = [
            row["id"] for row in await transaction.fetch("SELECT id FROM loaded_tag")
        ]
    return _loaded_tags


# The following tags might not be populated yet, e.g. Scans require a manual refresh from Product Opener
# Where off-query can fetch the data itself then new data is populated as part of migrations
# so there is no need to list these tags here
PARTIAL_TAGS = []


def check_tag_is_loaded(tag: str, loaded_tags):
    """Determine if data for a tag is available to query"""
    if tag.startswith(f"{NUTRIENT_TAG}.") or tag.startswith(f"{NUTRITION_TAG}."):
        return
    if tag not in list(TAG_TABLES.keys()) + PARTIAL_TAGS:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, f"Invalid field '{tag}'"
        )

    if tag in PARTIAL_TAGS and tag not in loaded_tags:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, f"Tag '{tag}' is not loaded"
        )


async def append_loaded_tags(transaction, new_tags: List[str]):
    global _loaded_tags
    if _loaded_tags == None:
        await get_loaded_tags(transaction)

    for tag in new_tags:
        if tag not in _loaded_tags:
            _loaded_tags.append(tag)
            await transaction.execute("INSERT INTO loaded_tag (id) VALUES ($1)", tag)
