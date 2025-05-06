from unittest.mock import patch

from ..models.health import HealthItemStatusEnum, HealthStatusEnum
from ..services.health import check_health
from ..test_helper import error_cursor, mock_cursor, patch_context_manager
from . import health


@patch.object(health, "find_products")
async def test_health_should_return_healthy(mocked_mongo):
    patch_context_manager(mocked_mongo, mock_cursor([]))
    my_health = await check_health()
    assert mocked_mongo.called
    assert my_health.status == HealthStatusEnum.ok
    assert my_health.info["postgres"].status == HealthItemStatusEnum.up
    assert my_health.info["mongodb"].status == HealthItemStatusEnum.up
    assert my_health.info["redis"].status == HealthItemStatusEnum.up


@patch.object(health, "find_products")
async def test_health_should_return_unhealthy_if_mongodb_is_down(mocked_mongo):
    patch_context_manager(mocked_mongo, error_cursor("mongodb is down"))
    my_health = await check_health()
    assert mocked_mongo.called
    assert my_health.status == HealthStatusEnum.error
    assert my_health.info["postgres"].status == HealthItemStatusEnum.up
    assert my_health.info["mongodb"].status == HealthItemStatusEnum.down
