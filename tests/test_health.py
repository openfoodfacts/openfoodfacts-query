from unittest.mock import patch
from query.main import HealthStatusEnum, health

async def test_health_ok():
    my_health = await health()
    assert my_health.status == HealthStatusEnum.ok
    

@patch("query.main.AsyncIOMotorClient", side_effect=Exception('mongodb is down'))
async def test_health_should_return_unhealthy_if_mongodb_is_down(mocked_mongo):
    my_health = await health()
    assert mocked_mongo.called
    assert my_health.status == HealthStatusEnum.error
