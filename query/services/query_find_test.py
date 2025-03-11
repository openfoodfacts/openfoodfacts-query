from query.database import database_connection
from query.models.country import Country
from query.models.query import Filter, FindQuery
from query.models.scans_by_country import ScansByCountry
from query.services import query
from query.services.query_count_test import create_test_tags
from query.tables.country import create_country
from query.tables.product_scans_by_country import create_scans
from query.test_helper import random_code


async def test_sorts_by_world_scans():
    async with database_connection() as connection:
        tags = await create_test_tags(connection)
        
        country = Country(tag=random_code(),code=random_code())
        await create_country(connection, country)
        await create_scans(connection, [ScansByCountry(product=tags.product1, country=country, year=2024, unique_scans=10)])
        await create_scans(connection, [ScansByCountry(product=tags.product2, country=country, year=2024, unique_scans=100)])
        
        results = await query.find(FindQuery(filter=Filter(countries_tags=country.tag), projection={'code': True}, sort=[('popularity_key', -1)]))
        assert results.index(tags.product2.code) < results.index(tags.product1.code)
        
        