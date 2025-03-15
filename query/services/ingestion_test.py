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
from query.tables.product_tags import create_tag, get_tags
from query.tables.settings import set_last_updated
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
        assert product_existing['source'] == Source.event
        assert product_existing['last_processed'] == last_processed


#   it('should start importing from the last import', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       // given: last_updated setting already set
#       const settings = app.get(settings_service);
#       const start_from = new date(2023, 1, 1);
#       await settings.set_last_modified(start_from);
#       const { products } = test_products();
#       const import_service = app.get(import_service);

#       // when: doing an incremental import from mongo_db
#       mock_mongo_db(products);
#       find_calls.length = 0;
#       await import_service.import_from_mongo('');

#       // then: mongo find is called with the setting as a parameter
#       expect(find_calls).to_have_length(2); // called for normal an obsolete prodocuts
#       expect(find_calls[0][0].last_updated_t.$gt).to_be(
#         math.floor(start_from.get_time() / 1000),
#       );

#       expect(await settings.get_last_modified()).to_strict_equal(
#         new date(last_updated * 1000),
#       );
#     });
#   });

#   it('should cope with nul characters', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       // when: importing data containing nul characters
#       const { product_id_new } = test_products();
#       mock_mongo_db([
#         {
#           // this one will be new
#           code: product_id_new,
#           last_updated_t: 1692032161,
#           ingredients_tags: ['test \u0000 test2 \u0000 end'],
#         },
#       ]);
#       await app.get(import_service).import_from_mongo();

#       // then: product should be loaded with nuls stripped
#       const ingredients_new = await app
#         .get(entity_manager)
#         .find(product_ingredients_tag, {
#           product: { code: product_id_new },
#         });

#       expect(ingredients_new).to_have_length(1);
#       expect(ingredients_new[0].value).to_be('test  test2  end');
#     });
#   });

#   it('should set last_updated correctly if one product has an invalid date', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       // given: products with invalid date
#       const settings = app.get(settings_service);
#       const start_from = new date(2023, 1, 1);
#       await settings.set_last_modified(start_from);
#       const { products } = test_products();
#       const test_data = [
#         products[0],
#         { ...products[1], last_updated_t: 'invalid' },
#       ];
#       const import_service = app.get(import_service);

#       // when: doing an import from mongo_db
#       mock_mongo_db(test_data);
#       await import_service.import_from_mongo('');

#       // then: the last modified date is set correctly
#       expect(await settings.get_last_modified()).to_strict_equal(
#         new date(last_updated * 1000),
#       );
#     });
#   });

#   it('should skip if already importing', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       // given: import already running
#       const import_service = app.get(import_service);
#       const { products } = test_products();
#       mock_mongo_db(products);
#       const first_import = import_service.import_from_mongo();
#       const warn_spy = jest.spy_on(import_service['logger'], 'warn');

#       // when: doing a second import
#       await import_service.import_from_mongo();
#       await first_import;

#       // then: second import just logs a warning
#       expect(warn_spy).to_have_been_called_times(1);
#     });
#   });

#   it('should cope with duplicate product codes', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       // when: importing data containing nul characters
#       const { product_id_new } = test_products();
#       const product_with_ingredients = {
#         code: product_id_new,
#         ingredients: [{ ingredient_text: 'test' }],
#       };
#       const duplicate_products = [
#         product_with_ingredients,
#         product_with_ingredients,
#       ];
#       mock_mongo_db(duplicate_products);
#       await app.get(import_service).import_from_mongo();

#       // then: product should be loaded with no duplicates
#       const ingredients_new = await app
#         .get(entity_manager)
#         .find(product_ingredient, {
#           product: { code: product_id_new },
#         });

#       expect(ingredients_new).to_have_length(1);
#       expect(ingredients_new[0].ingredient_text).to_be('test');
#     });
#   });

#   it('import from redis should always update product', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       // given: product with data that matches mongo_db
#       const em = app.get(entity_manager);
#       const last_processed = new date(2023, 1, 1);
#       const { products, product_id_existing } = test_products();
#       em.create(product, {
#         code: product_id_existing,
#         source: product_source.incremental_load,
#         process_id: 10n,
#         last_processed: last_processed,
#         last_updated: new date(last_updated * 1000),
#       });
#       await em.flush();
#       const import_service = app.get(import_service);

#       // when: doing an event import
#       mock_mongo_db(products);
#       await import_service.import_with_filter(
#         { code: { $in: [product_id_existing] } },
#         product_source.event,
#       );

#       // then: source is updated
#       const product_existing = await em.find_one(product, {
#         code: product_id_existing,
#       });
#       expect(product_existing).to_be_truthy();
#       expect(product_existing.source).to_be(product_source.event);
#       expect(product_existing.process_id).not.to_be(10n.to_string());
#       expect(product_existing.last_processed).not.to_strict_equal(last_processed);
#     });
#   });
# });

# describe('scheduled_import_from_mongo', () => {
#   it('should do a full import if loaded tags arent complete', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const import_service = app.get(import_service);
#       jest
#         .spy_on(app.get(tag_service), 'get_loaded_tags')
#         .mock_implementation(async () => []);
#       const import_spy = jest
#         .spy_on(import_service, 'import_from_mongo')
#         .mock_implementation();
#       await import_service.scheduled_import_from_mongo();
#       expect(import_spy).to_have_been_called_times(1);
#       expect(import_spy.mock.calls[0][0]).to_be_undefined();
#     });
#   });

#   it('should do an incremental import if loaded tags are complete', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const import_service = app.get(import_service);
#       jest
#         .spy_on(app.get(tag_service), 'get_loaded_tags')
#         .mock_implementation(async () => [
#           'dummy_tag', // add an extra tag to ensure this doesn't break things
#           ...object.keys(product_tag_map.mapped_tags).reverse(),
#         ]);
#       const import_spy = jest
#         .spy_on(import_service, 'import_from_mongo')
#         .mock_implementation();
#       await import_service.scheduled_import_from_mongo();
#       expect(import_spy).to_have_been_called_times(1);
#       expect(import_spy.mock.calls[0][0]).to_be('');
#     });
#   });
# });

# describe('product_tag', () => {
#   it('should add class to tag array', async () => {
#     await create_testing_module([domain_module], async () => {
#       expect(product_tag_map.mapped_tags['categories_tags']).to_be_truthy();
#     });
#   });
# });

# describe('import_with_filter', () => {
#   it('should not get an error with concurrent imports', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const import_service = app.get(import_service);

#       // when: doing an incremental import from mongo_db
#       const { products, product_id_existing, product_id_new } = test_products();
#       mock_mongo_db(products);
#       const imports = [];
#       // need more than 10 concurrent imports to start to see errors
#       for (let i = 0; i < 11; i++) {
#         imports.push(
#           import_service.import_with_filter(
#             { code: { $in: [product_id_existing, product_id_new] } },
#             product_source.event,
#           ),
#         );
#       }
#       await promise.all(imports);
#     });
#   });

#   it('should flag products not in mongodb as deleted', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const import_service = app.get(import_service);

#       // given: an existing product that doesn't exist in mongo_db
#       const em = app.get(entity_manager);
#       const product_id_to_delete = random_code();
#       const product_to_delete = em.create(product, {
#         code: product_id_to_delete,
#         source: product_source.full_load,
#         process_id: 10n,
#         last_processed: new date(2023, 1, 1),
#         last_updated: new date(last_updated * 1000),
#       });
#       em.create(product_ingredients_tag, {
#         product: product_to_delete,
#         value: 'old_ingredient',
#       });
#       await em.flush();

#       const before_import = date.now();
#       // when: doing an incremental import from mongo_db where the id is mentioned
#       const { products, product_id_existing, product_id_new } = test_products();
#       mock_mongo_db(products);
#       await import_service.import_with_filter(
#         { code: { $in: [product_id_existing, product_id_new, product_id_to_delete] } },
#         product_source.event,
#       );

#       // then: obsolete flag should get set to null
#       const deleted_product = await em.find_one(product, {
#         code: product_id_to_delete,
#       });
#       const updated_product = await em.find_one(product, {
#         code: product_id_existing,
#       });
#       expect(deleted_product.process_id).to_be(updated_product.process_id);
#       expect(deleted_product.last_processed.get_time()).to_be_greater_than_or_equal(
#         before_import,
#       );
#       expect(deleted_product.source).to_be(product_source.event);
#       expect(updated_product.obsolete).to_be(false);

#       const deleted_tag = await em.find_one(product_ingredients_tag, {
#         product: deleted_product,
#       });
#       expect(deleted_tag.obsolete).to_be_null();
#     });
#   });
# });
