from typing import List


async def create_table(connection):
    await connection.execute(
        "create table loaded_tag (id text not null, constraint loaded_tag_pkey primary key (id))",
    )
    await connection.execute(
        "insert into loaded_tag (id) values ('countries_tags'),('nutrition_grades_tags'),('nova_groups_tags'),('ecoscore_tags'),('brands_tags'),('categories_tags'),('labels_tags'),('packaging_tags'),('origins_tags'),('manufacturing_places_tags'),('emb_codes_tags'),('ingredients_tags'),('additives_tags'),('vitamins_tags'),('minerals_tags'),('amino_acids_tags'),('nucleotides_tags'),('other_nutritional_substances_tags'),('allergens_tags'),('traces_tags'),('misc_tags'),('languages_tags'),('states_tags'),('data_sources_tags'),('entry_dates_tags'),('last_edit_dates_tags'),('last_check_dates_tags'),('teams_tags') on conflict do nothing",
    )


_loaded_tags: List[str] | None = None


async def get_loaded_tags(connection):
    global _loaded_tags
    if _loaded_tags == None:
        _loaded_tags = [
            row["id"] for row in await connection.fetch("SELECT id FROM loaded_tag")
        ]
    return _loaded_tags


async def append_loaded_tags(connection, new_tags: List[str]):
    global _loaded_tags
    if _loaded_tags == None:
        await get_loaded_tags(connection)

    for tag in new_tags:
        if tag not in _loaded_tags:
            _loaded_tags.append(tag)
            await connection.execute("INSERT INTO loaded_tag (id) VALUES ($1)", tag)
