from ..tables import (
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
from ..views import product_updates_by_owner, views


async def up(transaction):
    await product.create_table(transaction)
    await product_tags.create_tables_v1(transaction)
    await loaded_tag.create_table(transaction)
    await product_ingredient.create_table(transaction)
    await settings.create_table(transaction)
    await product_update_event.create_table(transaction)
    await contributor.create_table(transaction)
    await update_type.create_table(transaction)
    await product_update.create_table(transaction)

    await views.create_schema(transaction)
    await product_updates_by_owner.create_view(transaction)
