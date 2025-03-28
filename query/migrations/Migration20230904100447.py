from query.tables import (
    contributor,
    loaded_tag,
    product,
    product_ingredient,
    product_tags,
    product_update,
    product_update_event,
    settings,
    update_type,
)
from query.views import product_updates_by_owner, views


async def up(connection):
    await product.create_table(connection)
    await product_tags.create_tables(connection)
    await loaded_tag.create_table(connection)
    await product_ingredient.create_table(connection)
    await settings.create_table(connection)
    await product_update_event.create_table(connection)
    await contributor.create_table(connection)
    await update_type.create_table(connection)
    await product_update.create_table(connection)

    await views.create_schema(connection)
    await product_updates_by_owner.create_view(connection)
