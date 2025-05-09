"""The root table for product information"""

import re
from datetime import datetime, timezone

from asyncpg import Connection

from ..database import create_record, get_rows_affected
from ..models.product import Source
from ..tables.product_ingredient import delete_ingredients
from ..tables.product_tags import TAG_TABLES, delete_tags

product_fields_column_mapping = {
    "code": "code",
    "product_name": "name",
    "creator": "creator",
    "owners_tags": "owners_tags",
    "last_modified_t": None,  # Note we actually use last_updated_t for checks but not all products may have this
    "last_updated_t": "last_updated",
    "ingredients_n": "ingredients_count",
    "ingredients_without_ciqual_codes_n": "ingredients_without_ciqual_codes_count",
    "ingredients": None,
    "rev": "revision",
}


def stored_root_product_fields():
    """Product fields that are stored on the root table"""
    return [key for key, value in product_fields_column_mapping.items() if value]


def get_product_column_for_field(field):
    """The column name for the corresponding MonoDB field name"""
    return product_fields_column_mapping.get(field, None)


def product_fields():
    """All of the MongoDB product document properties that are currently supported"""
    return list(TAG_TABLES.keys()) + stored_root_product_fields()


async def create_table(transaction: Connection):
    await transaction.execute(
        """create table product (
            id serial not null,
            name text null,
            code text null,
            last_updated timestamptz null,
            creator text null,
            owners_tags text null,
            obsolete boolean null default false,
            ingredients_without_ciqual_codes_count int null,
            ingredients_count int null,
            last_processed timestamptz null,
            source varchar(255) null,
            revision int null,
            process_id bigint null,
            constraint product_pkey primary key (id));""",
    )
    await transaction.execute(
        "create index product_code_index on product (code);",
    )
    await transaction.execute(
        "create index product_process_id_index on product (process_id);"
    )
    await transaction.execute(
        "create index product_creator_index on product (creator);"
    )
    await transaction.execute(
        "create index product_owners_tags_index on product (owners_tags);"
    )


async def update_products_from_staging(
    transaction: Connection, log, obsolete, process_id, source
):
    """Apply updates to products from the product_temp table. Assumes that a minimal product record has already been created"""
    product_results = await transaction.execute(
        f"""
      update product
      set name = tp.data->>'product_name',
        creator = tp.data->>'creator',
        owners_tags = tp.data->>'owners_tags',
        obsolete = $1,
        ingredients_count = (tp.data->>'ingredients_n')::numeric,
        ingredients_without_ciqual_codes_count = (tp.data->>'ingredients_without_ciqual_codes_n')::numeric,
        last_updated = tp.last_updated,
        process_id = $2,
        last_processed = $3,
        source = $4,
        revision = (tp.data->>'rev')::int
      from product_temp tp
      where product.id = tp.id""",
        obsolete,
        process_id,
        datetime.now(timezone.utc),
        source,
    )
    log(f"Updated {get_rows_affected(product_results)} products")


async def get_minimal_product(transaction, code):
    return await transaction.fetchrow(
        "SELECT id, last_updated FROM product WHERE code = $1", code
    )


async def create_minimal_product(transaction, code):
    return await transaction.fetchrow(
        "INSERT INTO product (code) VALUES ($1) RETURNING id", code
    )


async def create_product(transaction, **params):
    return await create_record(transaction, "product", **params)


async def get_product(transaction: Connection, code):
    return await transaction.fetchrow("SELECT * FROM product WHERE code = $1", code)


async def get_product_by_id(transaction, id):
    return await transaction.fetchrow("SELECT * FROM product WHERE id = $1", id)


async def delete_products(transaction, process_id, source, codes=None):
    """Soft delete all products and related data that were either not in the process (for a full load)
    or is one of the codes listed (for an event load)"""
    args = [process_id, datetime.now(timezone.utc), source]
    if codes:
        args.append(codes)
    results = await transaction.fetch(
        f"""UPDATE product SET 
                obsolete = NULL,
                process_id = $1,
                last_processed = $2,
                source = $3 
            WHERE obsolete IS NOT NULL
                {"AND process_id < $1" if source == Source.full_load else ""}
                {"AND code = ANY($4)" if codes else ""}
            RETURNING id""",
        *args,
    )
    deleted_ids = [result["id"] for result in results]
    await delete_tags(transaction, deleted_ids)
    await delete_ingredients(transaction, deleted_ids)


all_digits = re.compile(r"^\d+$")
leading_digits = re.compile(r"^0+")


def normalize_code(code):
    """Normalizes the length of a product code"""
    # Logic re-created from https://github.com/openfoodfacts/openfoodfacts-server/blob/main/lib/ProductOpener/Products.pm#L313
    # Return the code as-is if it is not all digits
    if not all_digits.match(code):
        return code

    # Remove leading zeroes
    code = leading_digits.sub("", code)

    # Add leading zeroes to have at least 13 digits
    code = code.zfill(13)

    #  Remove leading zeroes for EAN8s to keep only 8 digits
    if len(code) == 13 and code.startswith("00000"):
        code = code[5:]

    return code
