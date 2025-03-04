from query.tables import (
    product,
    product_tags,
    loaded_tag,
    product_ingredient,
    settings,
    product_update_event,
    contributor,
    update_type,
    product_update,
)

from query.views import views, product_updates_by_owner


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
