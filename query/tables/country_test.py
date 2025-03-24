from query.database import database_connection
from query.tables.country import add_all_countries


async def test_add_all_countries():
    async with database_connection() as connection:
        await connection.execute("insert into country (tag) values ('en:france') on conflict (tag) do update set code = null")
        await add_all_countries(connection)
        countries = await connection.fetch("select * from country")
        assert len(countries) > 100
        fr = next(c for c in countries if c['tag'] == 'en:france')
        assert fr
        assert fr['code'] == 'fr'
