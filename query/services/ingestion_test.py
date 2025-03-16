import asyncio
from datetime import datetime, timezone
import math
import time
from unittest.mock import Mock, patch
from query.database import database_connection
from query.models.product import Product, Source
from query.services import ingestion
from query.tables.country import get_country
from query.tables.product import create_product, get_product
from query.tables.product_country import create_product_country, get_product_countries
from query.tables.product_ingredient import get_ingredients
from query.tables.product_tags import create_tag, get_tags, tag_tables
from query.tables.settings import get_last_updated, set_last_updated
from query.test_helper import mock_cursor, patch_context_manager, random_code


async def test_get_process_id_is_monotonically_increasing():
    async with database_connection() as connection:
        transaction_id = await ingestion.get_process_id(connection)
        assert await ingestion.get_process_id(connection) > transaction_id


last_updated = 1692032161


def get_test_products():
    return [
        {
            # this one will be new
            "code": random_code(),
            "last_updated_t": last_updated,
            "ingredients_tags": ["test"],
            "rev": 1,
        },
        {
            # this one will already exist
            "code": random_code(),
            "last_updated_t": last_updated,
            "ingredients_tags": ["new_ingredient", "old_ingredient"],
            "countries_tags": ["en:france", random_code()],
        },
    ]


@patch("query.services.ingestion.find_products")
@patch("query.services.ingestion.get_process_id")
@patch("query.services.ingestion.append_loaded_tags")
async def test_import_from_mongo_should_import_a_new_product_update_existing_products_and_delete_missing_products(
    append_loaded_tags: Mock, get_process_id_mock: Mock, find_products_mock: Mock
):
    async with database_connection() as connection:
        # mock the process id so it doesn't delete records from other tests
        current_process_id = 0

        def next_process_id(_):
            nonlocal current_process_id
            current_process_id += 1
            return current_process_id

        get_process_id_mock.side_effect = next_process_id

        # given: two existing products, one of which is in mongo plus one new one in mongo
        products = get_test_products()
        product_existing = await create_product(
            connection, Product(code=products[1]["code"], process_id=0)
        )
        await create_tag(
            connection, "ingredients_tags", product_existing, "old_ingredient"
        )
        world = await get_country(connection, "en:world")
        await create_product_country(connection, product_existing, world, 10, 100)

        product_unchanged = await create_product(
            connection, Product(code=random_code(), process_id=0)
        )
        await create_tag(
            connection, "ingredients_tags", product_unchanged, "unchanged_ingredient"
        )

        # simulate a product that was added after the full load started
        product_later = await create_product(
            connection, Product(code=random_code(), process_id=100)
        )

        # when:doing a full import from mongo_db
        patch_context_manager(find_products_mock, mock_cursor(products))
        start = datetime.now(timezone.utc)

        await ingestion.import_from_mongo()

        # MongoDB called with no filter
        assert find_products_mock.call_args[0][0] == {}

        # then: new product is added, updated product is updated and other product is unchanged
        product_new = await get_product(connection, products[0]["code"])
        assert product_new
        assert product_new["process_id"] == current_process_id
        assert product_new["source"] == Source.full_load
        assert product_new["last_processed"] >= start
        assert product_new["revision"] == 1
        ingredients_new = await get_tags(
            connection, "ingredients_tags", product_new["id"]
        )
        assert len(ingredients_new) == 1
        assert ingredients_new[0]["value"] == "test"

        # should create at least a world entry in the product_country table
        countries = await get_product_countries(connection, product_new["id"])
        assert len(countries) == 1
        assert countries[0]["country_id"] == world.id
        assert countries[0]["obsolete"] == False

        ingredients_existing = await get_tags(
            connection, "ingredients_tags", product_existing.id
        )
        assert len(ingredients_existing) == 2
        assert any(i for i in ingredients_existing if i["value"] == "old_ingredient")
        assert any(i for i in ingredients_existing if i["value"] == "new_ingredient")

        # should create an entry for each country plus world
        countries_existing = await get_product_countries(
            connection, product_existing.id
        )
        assert len(countries_existing) == 3
        existing_world = next(
            (c for c in countries_existing if c["country_id"] == world.id), None
        )
        assert existing_world
        existing_world["recent_scans"] == 10
        france = await get_country(connection, "en:france")
        assert any(c for c in countries_existing if c["country_id"] == france.id)
        # creates the new country on-the-fly
        new_country_tag = products[1]["countries_tags"][1]
        new_country = await get_country(connection, new_country_tag)
        assert any(c for c in countries_existing if c["country_id"] == new_country.id)

        # check unchanged product has been "deleted"
        found_old_product = await get_product(connection, product_unchanged.code)
        assert found_old_product["obsolete"] == None
        ingredients_unchanged = await get_tags(
            connection, "ingredients_tags", product_unchanged.id
        )
        assert ingredients_unchanged[0]["obsolete"] == None

        found_later_product = await get_product(connection, product_later.code)
        assert found_later_product["obsolete"] == False

        assert append_loaded_tags.called


@patch("query.services.ingestion.find_products")
@patch("query.services.ingestion.append_loaded_tags")
async def test_incremental_import_should_not_update_loaded_tags(
    set_loaded_tags_mock, find_products_mock: Mock
):
    async with database_connection() as connection:
        # when: doing an incremental import from mongo_db
        products = get_test_products()
        patch_context_manager(find_products_mock, mock_cursor(products))

        last_updated = datetime.now(timezone.utc)
        await set_last_updated(connection, last_updated)
        await ingestion.import_from_mongo("")

        # then: set loaded tags is not updated
        assert not set_loaded_tags_mock.called

        product_new = await get_product(connection, products[0]["code"])
        assert product_new
        assert product_new["source"] == Source.incremental_load

        # MongoDB called with the correct filter
        call_args = find_products_mock.call_args[0][0]
        assert call_args == {
            "last_updated_t": {"$gt": math.floor(last_updated.timestamp())}
        }


@patch("query.services.ingestion.find_products")
async def test_import_with_no_change_should_not_update_the_source(
    find_products_mock: Mock,
):
    async with database_connection() as connection:
        test = time.time()
        # given: product with data that matches mongo_db
        last_processed = datetime(2023, 1, 1, tzinfo=timezone.utc)
        products = get_test_products()
        existing_product_code = products[1]["code"]
        await create_product(
            connection,
            Product(
                code=existing_product_code,
                source=Source.event,
                last_processed=last_processed,
                last_updated=datetime.fromtimestamp(last_updated, timezone.utc),
            ),
        )

        # when: doing an incremental import from mongo_db
        patch_context_manager(find_products_mock, mock_cursor(products))
        await ingestion.import_from_mongo("")

        # then: source is not updated
        product_existing = await get_product(connection, existing_product_code)
        assert product_existing
        assert product_existing["source"] == Source.event
        assert product_existing["last_processed"] == last_processed


@patch("query.services.ingestion.find_products")
async def test_start_importing_from_the_last_import(
    find_products_mock: Mock,
):
    async with database_connection() as connection:
        # given: last_updated setting already set
        start_from = datetime(2023, 1, 1, tzinfo=timezone.utc)
        await set_last_updated(connection, start_from)

        # when: doing an incremental import from mongo_db
        products = get_test_products()
        patch_context_manager(find_products_mock, mock_cursor(products))
        await ingestion.import_from_mongo("")

        # MongoDB called with the correct filter
        call_args = find_products_mock.call_args[0][0]
        assert call_args == {
            "last_updated_t": {"$gt": math.floor(start_from.timestamp())}
        }

        assert (await get_last_updated(connection)) == datetime.fromtimestamp(
            last_updated, timezone.utc
        )


@patch("query.services.ingestion.find_products")
async def test_cope_with_nul_characters(
    find_products_mock: Mock,
):
    async with database_connection() as connection:
        # when: importing data containing nul characters
        product_code = random_code()
        patch_context_manager(
            find_products_mock,
            mock_cursor(
                [
                    {
                        "code": product_code,
                        "last_updated_t": 1692032161,
                        "ingredients_tags": ["test \0 test2 \0 end"],
                    }
                ]
            ),
        )
        await ingestion.import_from_mongo("")

        # then: product should be loaded with nuls stripped
        product = await get_product(connection, product_code)
        ingredients = await get_tags(connection, "ingredients_tags", product["id"])

        assert len(ingredients) == 1
        assert ingredients[0]["value"] == "test  test2  end"


@patch("query.services.ingestion.find_products")
async def test_set_last_updated_correctly_if_one_product_has_an_invalid_date(
    find_products_mock: Mock,
):
    async with database_connection() as connection:
        # given: products with invalid date
        start_from = datetime(2023, 1, 1, tzinfo=timezone.utc)
        await set_last_updated(connection, start_from)
        products = get_test_products()
        invalid_product = dict(products[1])
        invalid_product["last_updated_t"] = "invalid"

        # when: doing an import from mongo_db
        patch_context_manager(
            find_products_mock, mock_cursor([products[0], invalid_product])
        )
        await ingestion.import_from_mongo("")

        # then: the last modified date is set correctly
        assert (await get_last_updated(connection)) == datetime.fromtimestamp(
            last_updated, timezone.utc
        )


@patch("query.services.ingestion.logger")
@patch("query.services.ingestion.find_products")
async def test_skip_if_already_importing(
    find_products_mock: Mock,
    logger_mock: Mock,
):
    # given: import already running
    products = get_test_products()
    patch_context_manager(find_products_mock, mock_cursor(products))
    # Note, don't await. In python need to use create_task to ensure the routine actually starts
    first_import = asyncio.create_task(ingestion.import_from_mongo("2000-01-01"))

    # when: doing a second import
    await ingestion.import_from_mongo("2001-01-01")
    await first_import

    # then: second import just logs a warning
    assert logger_mock.warning.called


@patch("query.services.ingestion.find_products")
async def test_cope_with_duplicate_product_codes(
    find_products_mock: Mock,
):
    async with database_connection() as connection:
        # when: importing data containing duplicate product codes
        product = {
            "code": random_code(),
            "ingredients": [{"text": "test"}],
        }
        patch_context_manager(find_products_mock, mock_cursor([product, product]))
        await ingestion.import_from_mongo("")

        found_products = await connection.fetch(
            "SELECT * FROM product WHERE code = $1", product["code"]
        )
        assert len(found_products) == 1

        ingredients = await get_ingredients(connection, found_products[0]["id"])
        assert len(ingredients) == 1
        assert ingredients[0]["ingredient_text"] == "test"


@patch("query.services.ingestion.find_products")
async def test_import_from_event_source_should_always_update_product(
    find_products_mock: Mock,
):
    async with database_connection() as connection:
        # given: product with data that matches mongo_db
        last_processed = datetime(2023, 1, 1, tzinfo=timezone.utc)
        products = get_test_products()
        product_code = products[1]["code"]
        await create_product(
            connection,
            Product(
                code=product_code,
                source=Source.incremental_load,
                process_id=10,
                last_processed=last_processed,
                last_updated=datetime.fromtimestamp(last_updated, timezone.utc),
            ),
        )
        patch_context_manager(find_products_mock, mock_cursor(products))
        await ingestion.import_with_filter(
            {"code": {"$in": [product_code]}}, Source.event
        )

        # then: source is updated
        product_existing = await get_product(connection, product_code)
        assert product_existing
        assert product_existing["source"] == Source.event
        assert product_existing["process_id"] != 10
        assert product_existing["last_processed"] > last_processed


@patch("query.services.ingestion.get_loaded_tags", return_value=[])
@patch("query.services.ingestion.import_from_mongo")
async def test_scheduled_import_from_mongo_should_do_a_full_import_if_loaded_tags_arent_complete(
    import_mock: Mock,
    _: Mock,
):
    await ingestion.scheduled_import_from_mongo()
    assert import_mock.called
    assert len(import_mock.call_args[0]) == 0


# add an extra tag to ensure this doesn't break things
@patch(
    "query.services.ingestion.get_loaded_tags",
    return_value=list(tag_tables.keys()) + ["dummy_tag"],
)
@patch("query.services.ingestion.import_from_mongo")
async def test_scheduled_import_from_mongo_should_do_an_incremental_import_if_loaded_tags_are_complete(
    import_mock: Mock,
    _: Mock,
):
    await ingestion.scheduled_import_from_mongo()
    assert import_mock.called
    assert import_mock.call_args[0][0] == ""


async def test_not_get_an_error_with_concurrent_imports():
    products = get_test_products()

    async def one_import():
        with patch("query.services.ingestion.find_products") as find_products_mock:
            patch_context_manager(find_products_mock, mock_cursor(products))
            await ingestion.import_with_filter(
                {"code": {"$in": [products[0]["code"], products[1]["code"]]}},
                Source.event,
            )

    running_imports = []
    for i in range(11):
        running_imports.append(one_import())

    await asyncio.gather(*running_imports)
    async with database_connection() as connection:
        found_product = await connection.fetch(
            "SELECT * FROM product WHERE code = $1", products[0]["code"]
        )
        assert len(found_product) == 1


@patch("query.services.ingestion.find_products")
async def test_event_load_should_flag_products_not_in_mongodb_as_deleted(
    find_products_mock: Mock,
):
    async with database_connection() as connection:
        # given: an existing product that doesn't exist in mongo_db
        product_code_to_delete = random_code()
        product_to_delete = await create_product(
            connection,
            Product(
                code=product_code_to_delete,
                source=Source.full_load,
                process_id=10,
                last_processed=datetime(2023, 1, 1, tzinfo=timezone.utc),
                last_updated=datetime.fromtimestamp(last_updated, timezone.utc),
            ),
        )
        await create_tag(
            connection, "ingredients_tags", product_to_delete, "old_ingredient"
        )

        before_import = datetime.now(timezone.utc)

        # when: doing an incremental import from mongo_db where the id is mentioned
        products = get_test_products()
        patch_context_manager(find_products_mock, mock_cursor(products))
        await ingestion.import_with_filter(
            {
                "code": {
                    "$in": [
                        products[0]["code"],
                        products[1]["code"],
                        product_code_to_delete,
                    ]
                }
            },
            Source.event,
        )

        # then: obsolete flag should get set to null
        deleted_product = await get_product(connection, product_code_to_delete)
        updated_product = await get_product(connection, products[1]["code"])
        assert deleted_product["process_id"] == updated_product["process_id"]
        assert deleted_product["last_processed"] >= before_import
        assert deleted_product["source"] == Source.event
        assert updated_product["obsolete"] == False

        deleted_tags = await get_tags(
            connection, "ingredients_tags", deleted_product["id"]
        )
        assert len(deleted_tags) == 1
        assert deleted_tags[0]["obsolete"] == None


@patch("query.services.ingestion.find_products")
async def test_import_from_obsolete_collection(find_products_mock: Mock):
    async with database_connection() as connection:
        # given: one existing product
        products = get_test_products()
        product_existing = await create_product(
            connection, Product(code=products[1]["code"], process_id=0)
        )
        await create_tag(
            connection, "ingredients_tags", product_existing, "old_ingredient"
        )
        await create_tag(
            connection, "ingredients_tags", product_existing, "to_be_deleted"
        )

        # when importing from mongodb where existing product is obsolete then it is marked as such
        patch_context_manager(
            find_products_mock, mock_cursor([products[0]]), mock_cursor([products[1]])
        )
        await ingestion.import_with_filter({}, Source.incremental_load)

        # MongoDB is called twice. Second time for the obsolete collection
        call_args_list = find_products_mock.call_args_list
        assert len(call_args_list) == 2
        assert call_args_list[0][0][2] == False
        assert call_args_list[1][0][2] == True

        found_product = await get_product(connection, product_existing.code)
        assert found_product["obsolete"] == True
        found_tags = await get_tags(connection, "ingredients_tags", found_product["id"])
        assert all(tag for tag in found_tags if tag["obsolete"] == True)
        assert (
            any(tag for tag in found_tags if tag["value"] == "to_be_deleted") == False
        )

        new_product = await get_product(connection, products[0]["code"])
        assert new_product["obsolete"] == False
        assert found_product["process_id"] == new_product["process_id"]


@patch("query.services.ingestion.find_products")
async def test_all_supported_fields(find_products_mock: Mock):
    async with database_connection() as connection:
        # when importing from mongodb where all fields are populated
        test_product = {
            "code": random_code(),
            "product_name": "test name",
            "last_updated_t": last_updated,
            "last_modified_t": last_updated - 1,
            "creator": "test creator",
            "owners_tags": "test owners tags",
            "ingredients_n": 3,
            "ingredients_without_ciqual_codes_n": 2,
            "rev": 123,
            "ingredients": [
                {
                    "text": "first ingredient",
                    "id": "en:1",
                    "ciqual_food_code": "CFC1",
                    "percent": "50",
                    "percent_min": 20,
                    "percent_max": 70,
                    "percent_estimate": 51,
                },
                {
                    "text": "second parent",
                    "ingredients": [
                        {"text": "child of second ingredient", "id": "en:2.1"}
                    ],
                },
            ],
        }
        patch_context_manager(find_products_mock, mock_cursor([test_product]))
        await ingestion.import_with_filter({}, Source.incremental_load)
        
        found_product = await get_product(connection, test_product['code'])
        assert found_product['name'] == test_product['product_name']
        assert found_product['last_updated'] == datetime.fromtimestamp(last_updated, timezone.utc)
        assert found_product['creator'] == test_product['creator']
        assert found_product['owners_tags'] == test_product['owners_tags']
        assert found_product['ingredients_count'] == test_product['ingredients_n']
        assert found_product['ingredients_without_ciqual_codes_count'] == test_product['ingredients_without_ciqual_codes_n']
        assert found_product['revision'] == test_product['rev']

        found_ingredients = await get_ingredients(connection, found_product['id'])
        assert len(found_ingredients) == 3
        first_ingredient = next(i for i in found_ingredients if i['ingredient_text'] == "first ingredient")
        assert first_ingredient
        test_first_ingredient = test_product['ingredients'][0]
        assert first_ingredient['sequence'] == '1'
        assert first_ingredient['id'] == test_first_ingredient['id']
        assert first_ingredient['ciqual_food_code'] == test_first_ingredient['ciqual_food_code']
        assert first_ingredient['percent'] == test_first_ingredient['percent']
        assert first_ingredient['percent_min'] == test_first_ingredient['percent_min']
        assert first_ingredient['percent_max'] == test_first_ingredient['percent_max']
        assert first_ingredient['percent_estimate'] == test_first_ingredient['percent_estimate']
        assert first_ingredient['parent_sequence'] == None
        
        second_ingredient = next(i for i in found_ingredients if i['ingredient_text'] == "second parent")
        assert second_ingredient
        assert second_ingredient['sequence'] == '2'
        assert second_ingredient['parent_sequence'] == None

        child_ingredient = next(i for i in found_ingredients if i['ingredient_text'] == "child of second ingredient")
        assert child_ingredient
        assert child_ingredient['sequence'] == '2.1'
        assert child_ingredient['parent_sequence'] == '2'
        assert child_ingredient['id'] == test_product['ingredients'][1]['ingredients'][0]['id']
        
