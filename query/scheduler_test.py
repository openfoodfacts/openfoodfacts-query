from unittest.mock import Mock, patch

from . import scheduler
from .scheduler import scheduled_import_from_mongo
from .tables.product_tags import TAG_TABLES


@patch.object(scheduler, "get_loaded_tags", return_value=[])
@patch.object(scheduler, "import_from_mongo")
@patch.object(scheduler, "stop_redis_listener")
@patch.object(scheduler, "start_redis_listener")
async def test_scheduled_import_from_mongo_should_do_a_full_import_if_loaded_tags_arent_complete(
    start_listener: Mock,
    stop_listener: Mock,
    import_mock: Mock,
    _: Mock,
):
    await scheduled_import_from_mongo()
    assert import_mock.called
    assert len(import_mock.call_args[0]) == 0
    assert stop_listener.called
    assert start_listener.called


# add an extra tag to ensure this doesn't break things
@patch.object(
    scheduler,
    "get_loaded_tags",
    return_value=list(TAG_TABLES.keys()) + ["dummy_tag"],
)
@patch.object(scheduler, "import_from_mongo")
async def test_scheduled_import_from_mongo_should_do_an_incremental_import_if_loaded_tags_are_complete(
    import_mock: Mock,
    _: Mock,
):
    await scheduled_import_from_mongo()
    assert import_mock.called
    assert import_mock.call_args[0][0] == ""
