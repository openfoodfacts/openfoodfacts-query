from unittest.mock import ANY, Mock, patch

from ..database import get_transaction
from ..models.scan import ProductScans
from ..services.scan import import_scans
from ..tables.country import add_all_countries
from ..tables.product import normalize_code
from ..tables.product_country import CURRENT_YEAR, OLDEST_YEAR, PRODUCT_COUNTRY_TAG
from ..test_helper import random_code
from . import scan


@patch.object(scan, "normalize_code", side_effect=normalize_code)
async def test_create_product_scans(normalize_code_wrapper: Mock):
    async with get_transaction() as transaction:
        # refresh country table
        await add_all_countries(transaction)

        # create some products
        code1 = random_code()
        code2 = random_code()
        ids = await transaction.fetch(
            "insert into product (code) values ($1),($2) returning id", code1, code2
        )

        # Add country records for UK and France but not ru
        for product in ids:
            await transaction.execute(
                "insert into product_countries_tag (product_id, value) values ($1, $2), ($1, $3)",
                product["id"],
                "en:united-kingdom",
                "en:france",
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
                        "unique_scans_n_by_country": {"uk": 1, "gb": 2, "world": 3},
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

    async with get_transaction() as transaction:
        result = await transaction.fetch(
            "select * from product_scans_by_country where product_id = (select id from product where code = $1)",
            code1,
        )
        assert len(result) == 7

        product_countries = await transaction.fetch(
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
        assert normalize_code_wrapper.called

        # Should not create product_country records for ru
        product_countries = await transaction.fetch(
            """select * from product_country pc
        join country c on c.id = pc.country_id 
        where product_id = (select id from product where code = $1)
        and c.code = 'ru'""",
            code2,
        )
        assert len(product_countries) == 0


@patch.object(scan, "append_loaded_tags")
async def test_update_tags_when_fully_loaded(append_loaded_tags: Mock):
    async with get_transaction() as transaction:
        # refresh country table
        await add_all_countries(transaction)

        # create a product
        code = random_code()
        await transaction.execute("insert into product (code) values ($1)", code)

        await import_scans(
            ProductScans.model_validate(
                {
                    code: {
                        str(CURRENT_YEAR): {
                            "scans_n": 10,
                            "unique_scans_n": 7,
                            "unique_scans_n_by_country": {"uk": 2, "fr": 5, "world": 7},
                        },
                    },
                }
            ),
            True,
        )

        append_loaded_tags.assert_called_with(ANY, [PRODUCT_COUNTRY_TAG])
