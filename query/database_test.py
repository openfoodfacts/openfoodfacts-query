from datetime import datetime, timezone
from query.database import database_connection, get_rows_affected


async def test_rows_affected_returned_correctly():
    async with database_connection() as connection:
        await connection.execute("CREATE TEMP TABLE product_temp (id int PRIMARY KEY, last_updated timestamptz, data jsonb)")
        result = await connection.execute("INSERT INTO product_temp (last_updated, id, data) VALUES ($1,$2,$3),($1,$4,$5),($1,$6,$7)", 
                                          datetime(2023,1,1, tzinfo=timezone.utc),
                                          1, {"a": 1},
                                          2, {"b": 2},
                                          3, {"c": 3},
                                          )

        assert get_rows_affected(result) == 3
        
        result = await connection.execute("UPDATE product_temp SET data = $1 WHERE id < $2", {"d":4}, 3)
        assert get_rows_affected(result) == 2
        
        result = await connection.execute("DELETE FROM product_temp WHERE id < $1", 3)
        assert get_rows_affected(result) == 2

