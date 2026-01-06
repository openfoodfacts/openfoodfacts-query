"""The root table for product information"""

import re
from datetime import datetime, timezone
from typing import List

from asyncpg import Connection

from query.models.scan import ProductScans
from query.tables.loaded_tag import PARTIAL_TAGS, check_tag_is_loaded
from query.tables.product_country import CURRENT_YEAR, delete_product_countries

from ..database import create_record, get_rows_affected
from ..models.product import Source
from ..tables.product_ingredient import delete_ingredients
from ..tables.product_tags import TAG_TABLES, delete_tags

PRODUCT_FIELD_BASE_COLUMNS = {
    "code": "code",
    "product_name": "name",
    "creator": "creator",
    "owners_tags": "owners_tags",
    "last_updated_t": "last_updated",
    "ingredients_n": "ingredients_count",
    "ingredients_without_ciqual_codes_n": "ingredients_without_ciqual_codes_count",
    "rev": "revision",
    "last_modified_t": "last_modified",  # Note we actually use last_updated_t to determine if a product has changed
    "created_t": "created",
    "completeness": "completeness",
    "nutriscore_score": "nutriscore",
    "nova_score": "nova_score",
    "environmental_score_score": "environmental_score",
    "ingredients_from_palm_oil_n": "ingredients_from_palm_oil_count",
    "ingredients_that_may_be_from_palm_oil_n": "ingredients_that_may_be_from_palm_oil_count",
    "additives_n": "additives_count",
    "ingredients_from_or_that_may_be_from_palm_oil_n": "ingredients_from_or_that_may_be_from_palm_oil_count",
}
PRODUCT_TAG = "product"

PRODUCT_FIELD_SCANS_COLUMNS = {
    "scans_n": "scan_count",
    "unique_scans_n": "unique_scan_count",
}
PRODUCT_SCANS_TAG = "product_scans"
PARTIAL_TAGS.append(PRODUCT_SCANS_TAG)

PRODUCT_FIELD_COLUMNS = PRODUCT_FIELD_BASE_COLUMNS | PRODUCT_FIELD_SCANS_COLUMNS


def stored_root_product_fields():
    """Product fields that are stored on the root table"""
    return [key for key, value in PRODUCT_FIELD_COLUMNS.items() if value]


def get_product_column_for_field(field, loaded_tags):
    """The column name for the corresponding MonoDB field name. Returns None if field isn't loaded yet"""
    column = PRODUCT_FIELD_BASE_COLUMNS.get(field, None)
    if not column:
        column = PRODUCT_FIELD_SCANS_COLUMNS.get(field, None)
        if column:
            check_tag_is_loaded(PRODUCT_SCANS_TAG, loaded_tags)

    return column


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
            last_modified timestamptz null,
            created timestamptz null,
            completeness double precision null,
            nutriscore int null,
            environmental_score int null,
            ingredients_from_palm_oil_count int null,
            ingredients_that_may_be_from_palm_oil_count int null,
            additives_count int null,
            ingredients_from_or_that_may_be_from_palm_oil_count int null,
            scan_count int null,
            unique_scan_count int,
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
    await transaction.execute(
        "create index product_created_index on product (created DESC NULLS LAST, id);",
    )
    await transaction.execute(
        "create index product_completeness_index on product (completeness, id);",
    )
    await transaction.execute(
        "create index product_nutriscore_index on product (nutriscore, id);",
    )
    await transaction.execute(
        "create index product_environmental_score_index on product (environmental_score DESC NULLS LAST, id);",
    )
    await transaction.execute(
        "create index product_name_index on product (name, id);",
    )
    await transaction.execute(
        "create index product_last_modified_index on product (last_modified DESC NULLS LAST, id);",
    )
    await transaction.execute(
        "create index product_scan_count_index on product (scan_count DESC NULLS LAST, id);",
    )
    await transaction.execute(
        "create index product_unique_scan_count_index on product (unique_scan_count DESC NULLS LAST, id);",
    )


async def update_products_from_staging(
    transaction: Connection, log, obsolete, process_id, source
):
    """Apply updates to products from the product_temp table. Assumes that a minimal product record has already been created"""

    # Don't update the source and last_updated date for partial updates
    params = [obsolete, process_id, datetime.now(timezone.utc)]

    last_updated_sql = ""
    if source != Source.partial:
        params.append(source)
        last_updated_sql = f"last_updated = tp.last_updated, source = $4,"

    # Note we cast as numeric rather than int in the SQL below as casting something like "2.0" as an int will fail
    product_results = await transaction.execute(
        f"""
      update product
      set name = tp.data->>'product_name',
        creator = tp.data->>'creator',
        owners_tags = tp.data->>'owners_tags',
        {last_updated_sql}
        obsolete = $1,
        ingredients_count = (tp.data->>'ingredients_n')::numeric,
        ingredients_without_ciqual_codes_count = (tp.data->>'ingredients_without_ciqual_codes_n')::numeric,
        created = to_timestamp((tp.data->>'created_t')::numeric),
        last_modified = to_timestamp((tp.data->>'last_modified_t')::numeric),
        completeness = (tp.data->>'completeness')::double precision,
        nutriscore = (tp.data->>'nutriscore_score')::numeric,
        environmental_score = (tp.data->>'environmental_score_score')::numeric,
        ingredients_from_palm_oil_count = (tp.data->>'ingredients_from_palm_oil_n')::numeric,
        ingredients_that_may_be_from_palm_oil_count = (tp.data->>'ingredients_that_may_be_from_palm_oil_n')::numeric,
        additives_count = (tp.data->>'additives_n')::numeric,
        ingredients_from_or_that_may_be_from_palm_oil_count = (tp.data->>'ingredients_from_or_that_may_be_from_palm_oil_n')::numeric,
        process_id = $2,
        last_processed = $3,
        revision = (tp.data->>'rev')::numeric
      from product_temp tp
      where product.id = tp.id""",
        *params,
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


async def create_minimal_product_from_events(transaction, event_ids: List[int]):
    """Create a product entry corresponding to cited product of a set of events
    
    This is useful for example when we import sample events in a database
    (for developers).
    """
    await transaction.execute(
        """INSERT INTO product (code)
      SELECT DISTINCT pe.message->>'code'
      FROM product_update_event pe
      where pe.id = ANY($1)
      AND NOT EXISTS (SELECT * FROM product p2 WHERE p2.code = pe.message->>'code')""",
        event_ids,
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
    await delete_product_countries(transaction, deleted_ids)


async def update_scans(transaction: Connection, scans: ProductScans):
    product_scans = []
    for code, years in scans.root.items():
        scan_counts = years.root.get(str(CURRENT_YEAR), None)
        if scan_counts:
            product_scans.append(
                [code, int(scan_counts.scans_n), int(scan_counts.unique_scans_n)]
            )
        else:
            product_scans.append(
                [code, 0, 0]
            )  # Always update the product so we can zero totals if there are no scans in the current year

    if product_scans:
        updated = await transaction.fetchmany(
            """UPDATE product
            SET scan_count = $2,
            unique_scan_count = $3
            WHERE code = $1
            RETURNING id""",
            product_scans,
        )
        return list({i["id"] for i in updated})

    return []


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
