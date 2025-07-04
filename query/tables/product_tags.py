"""The set of tables that store product tags. Each tag is simply an array of values on the product.
The order of tags is not preserved"""

from ..database import create_record, get_rows_affected

COUNTRIES_TAG = "countries_tags"
tag_tables_v1 = {
    "_keywords": "product_keywords_tag",
    "additives_tags": "product_additives_tag",
    "allergens_tags": "product_allergens_tag",
    "amino_acids_tags": "product_amino_acids_tag",
    "brands_tags": "product_brands_tag",
    "categories_properties_tags": "product_categories_properites_tag",
    "categories_tags": "product_categories_tag",
    "checkers_tags": "product_checkers_tag",
    "cities_tags": "product_cities_tag",
    "codes_tags": "product_codes_tag",
    "correctors_tags": "product_correctors_tag",
    COUNTRIES_TAG: "product_countries_tag",
    "data_quality_bugs_tags": "product_data_quality_bugs_tag",
    "data_quality_errors_tags": "product_data_quality_errors_tag",
    "data_quality_tags": "product_data_quality_tag",
    "data_quality_warnings_tags": "product_data_quality_warnings_tag",
    "data_sources_tags": "product_data_sources_tag",
    "debug_tags": "product_debug_tag",
    "ecoscore_tags": "product_ecoscore_tag",
    "editors_tags": "product_editors_tag",
    "emb_codes_tags": "product_emb_codes_tag",
    "entry_dates_tags": "product_entry_dates_tag",
    "food_groups_tags": "product_food_groups_tag",
    "informers_tags": "product_informers_tag",
    "ingredients_analysis_tags": "product_ingredients_analysis_tag",
    "ingredients_from_palm_oil_tags": "product_ingredients_from_palm_oil_tag",
    "ingredients_n_tags": "product_ingredients_ntag",
    "ingredients_original_tags": "product_ingredients_original_tag",
    "ingredients_tags": "product_ingredients_tag",
    "ingredients_that_may_be_from_palm_oil_tags": "product_ingredients_that_may_be_from_palm_oil_tag",
    "labels_tags": "product_labels_tag",
    "languages_tags": "product_languages_tag",
    "last_check_dates_tags": "product_last_check_dates_tag",
    "last_edit_dates_tags": "product_last_edit_dates_tag",
    "last_image_dates_tags": "product_latest_image_dates_tag",
    "manufacturing_places_tags": "product_manufacturing_places_tag",
    "minerals_tags": "product_minerals_tag",
    "misc_tags": "product_misc_tag",
    "nova_groups_tags": "product_nova_groups_tag",
    "nucleotides_tags": "product_nucleotides_tag",
    "nutrient_levels_tags": "product_nutrient_levels_tag",
    "nutriscore_2021_tags": "product_nutriscore2021tag",
    "nutriscore_2023_tags": "product_nutriscore2023tag",
    "nutriscore_tags": "product_nutriscore_tag",
    "nutrition_grades_tags": "product_nutrition_grades_tag",
    "origins_tags": "product_origins_tag",
    "other_nutritional_substances_tags": "product_other_nutritional_substances_tag",
    "packaging_materials_tags": "product_packaging_materials_tag",
    "packaging_recycling_tags": "product_packaging_recycling_tag",
    "packaging_shapes_tags": "product_packaging_shapes_tag",
    "packaging_tags": "product_packaging_tag",
    "periods_after_opening_tags": "product_periods_after_opening_tag",
    "photographers_tags": "product_photographers_tag",
    "pnns_groups_1_tags": "product_pnns_groups1tag",
    "pnns_groups_2_tags": "product_pnns_groups2tag",
    "popularity_tags": "product_popularity_tag",
    "purchase_places_tags": "product_purchase_places_tag",
    "states_tags": "product_states_tag",
    "stores_tags": "product_stores_tag",
    "teams_tags": "product_teams_tag",
    "traces_tags": "product_traces_tag",
    "unknown_nutrients_tags": "product_unknown_nutrients_tag",
    "vitamins_tags": "product_vitamins_tag",
    "weighers_tags": "product_weighers_tag",
}

# Append additional tag tables to this list when we introduce them and then add a migration to create the new tables
TAG_TABLES = tag_tables_v1


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
