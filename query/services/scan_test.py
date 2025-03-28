from query.database import database_connection
from query.models.scan import ProductScans
from query.services.scan import import_scans
from query.tables.country import add_all_countries
from query.tables.product_country import CURRENT_YEAR, OLDEST_YEAR
from query.test_helper import random_code


async def test_create_product_scans():
    async with database_connection() as connection:
        # refresh country table
        await add_all_countries(connection)

        # create some products
        code1 = random_code()
        code2 = random_code()
        await connection.execute(
            "insert into product (code) values ($1),($2)", code1, code2
        )

        await import_scans(
            ProductScans.model_validate(
                {
                    code1: {
                        # this one shouldn't be included in the totals
                        str(OLDEST_YEAR - 1): {
                            "scans_n": 3,
                            "unique_scans_n": 2,
                            "unique_scans_n_by_country": {"uk": 2, "world": 2},
                        },
                        str(OLDEST_YEAR): {
                            "scans_n": 7,
                            "unique_scans_n": 3,
                            "unique_scans_n_by_country": {"uk": 3, "world": 3},
                        },
                        str(CURRENT_YEAR): {
                            "scans_n": 10,
                            "unique_scans_n": 7,
                            "unique_scans_n_by_country": {"uk": 2, "fr": 5, "world": 7},
                        },
                    },
                    code2: {
                        str(CURRENT_YEAR): {
                            "scans_n": 11,
                            "unique_scans_n": 8,
                            "unique_scans_n_by_country": {"ru": 1, "fr": 4, "world": 5},
                        },
                    },
                }
            )
        )
        result = await connection.fetch(
            "select * from product_scans_by_country where product_id = (select id from product where code = $1)",
            code1,
        )
        assert len(result) == 7

        product_countries = await connection.fetch(
            """select * from product_country pc
        join country c on c.id = pc.country_id 
        where product_id = (select id from product where code = $1)
        and c.code = 'uk'""",
            code1,
        )
        assert len(product_countries) == 1
        assert product_countries[0]["recent_scans"] == 2
        assert product_countries[0]["total_scans"] == 5
        assert product_countries[0]["obsolete"] == False


#   it('should update tags when all loaded', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       scans_service = app.get(scans_service);

#       # create a product
#       code1 = random_code();
#       await sql`insert into product ${sql([
#         {
#           code: code1,
#         },
#       ])}`;

#       await scans_service.create(
#         {
#           [code1]: {
#             [scans_service.current_year]: {
#               scans_n: 10,
#               unique_scans_n: 7,
#               unique_scans_n_by_country: {
#                 uk: 2,
#                 fr: 5,
#                 world: 7,
#               },
#             },
#           },
#         },
#         true,
#       );
#       loaded_tags = await app.get(tag_service).get_loaded_tags();
#       expect(loaded_tags).to_contain(product_country.tag);
#     });
#   });
# });
