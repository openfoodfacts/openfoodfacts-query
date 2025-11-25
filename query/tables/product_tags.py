"""The set of tables that store product tags. Each tag is simply an array of values on the product.
The order of tags is not preserved"""

from ..database import create_record, get_rows_affected
from .product_tags_list import COUNTRIES_TAG, TAG_TABLES


async def create_tables(transaction, tag_tables):
    """Creates tag tables. Note this will need to be edited if new tags are added and a migration script added at the end to add the newer tables"""
    for table_name in tag_tables.values():
        await transaction.execute(
            f"""create table {table_name} (
                product_id int not null,
                value text not null,
                obsolete boolean null default false,
                constraint {table_name}_pkey primary key (value, product_id))""",
        )
        await transaction.execute(
            f"create index {table_name}_product_id_index on {table_name} (product_id);"
        )
        await transaction.execute(
            f"alter table {table_name} add constraint {table_name}_product_id_foreign foreign key (product_id) references product (id) on update cascade on delete cascade;",
        )


async def create_tables_v1(transaction):
    await create_tables(transaction, tag_tables_v1)


async def create_tag(transaction, tag, product, value):
    return await create_record(
        transaction,
        TAG_TABLES[tag],
        product_id=product["id"],
        value=value,
        obsolete=product["obsolete"],
    )


async def create_tags_from_staging(transaction, log, obsolete, tags):
    """Populates all of the tag tables from the product_temp data"""
    for tag in tags:
        tag_table = TAG_TABLES.get(tag, None)
        if tag_table:
            log_text = f"Updated {tag}"

            # Delete existing tags for products that were imported on this run
            deleted = await transaction.execute(
                f"""delete from {tag_table}
                where product_id in (select id from product_temp)"""
            )
            log_text += f" deleted {get_rows_affected(deleted)},"

            # Add tags back in with the updated information
            results = await transaction.execute(
                f"""insert into {tag_table} (product_id, value, obsolete)
            select DISTINCT id, tag.value, {obsolete} from product_temp 
            cross join jsonb_array_elements_text(data->'{tag}') tag"""
            )
            log_text += f" inserted {get_rows_affected(results)} rows"
            log(log_text)


async def delete_tags(transaction, product_ids):
    """Soft deletes tags for the specified products"""
    for tag_table in TAG_TABLES.values():
        await transaction.execute(
            f"UPDATE {tag_table} SET obsolete = NULL WHERE product_id = ANY($1::numeric[])",
            product_ids,
        )


async def get_tags(transaction, tag, product):
    tag_table = TAG_TABLES[tag]
    return await transaction.fetch(
        f"SELECT * FROM {tag_table} WHERE product_id = $1", product["id"]
    )
