import query.repositories.product as product
import query.repositories.product_tags as product_tags

async def up(connection):
    # Changing product id from a UUID to an integer. Migration steps are as follows:
    # 1. Drop all existing primary keys that reference product_id (CASCADE removes foreign keys too)
    # 2. Drop old value index
    # 3. Rename old product id column
    # 4. Add new integer product id column
    # 5. Update new column for tags
    # 6. Make column not null
    # 7. Add back primary keys
    # 8. Add product id index
    # 9. Add back foreign keys
    # 10. Drop old column

    # 1. Drop all existing primary keys that reference product_id (CASCADE removes foreign keys too)
    await product_tags.drop_old_id(connection)

    await connection.execute(
        "alter table query.product_ingredient DROP CONSTRAINT product_ingredient_pkey CASCADE;"
    )
    await product.change_primary_key(connection)

    # 2. Drop old value index
    # 3. Rename old product id column
    await connection.execute(
        "alter table query.product_ingredient RENAME COLUMN parent_product_id TO old_parent_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredient RENAME COLUMN product_id TO old_product_id;"
    )
    # 4. Add new integer product id column
    await connection.execute(
        "alter table query.product_ingredient ADD COLUMN parent_product_id int NULL;"
    )
    await connection.execute(
        "alter table query.product_ingredient ADD COLUMN product_id int NULL;"
    )

    # 5. Update new column for tags
    await product_tags.populate_new_product_id(connection)
    await connection.execute(
        "update query.product_ingredient set parent_product_id = product.id from query.product WHERE old_id = old_parent_product_id AND parent_product_id IS NULL;"
    )
    await connection.execute(
        "update query.product_ingredient set product_id = product.id from query.product WHERE old_id = old_product_id AND product_id IS NULL;"
    )
    # 6. Make column not null
    await connection.execute(
        "alter table query.product_ingredient alter column product_id SET NOT NULL;"
    )

    # 7. Add back primary keys
    await connection.execute(
        "alter table query.product_ingredient ADD CONSTRAINT product_ingredient_pkey PRIMARY KEY (product_id,sequence);"
    )

    # 8. Add product id index

    # 9. Add back foreign keys
    await connection.execute(
        'alter table query.product_ingredient add constraint product_ingredient_product_id_foreign FOREIGN KEY (product_id) references "product" ("id") on update cascade on delete cascade;'
    )

    # 10. Drop old column
    await connection.execute(
        "alter table query.product_ingredient drop column old_parent_product_id;"
    )
    await connection.execute(
        "alter table query.product_ingredient drop column old_product_id;"
    )
    await product.drop_old_id(connection)

    await connection.execute(
        'create index "product_ingredient_parent_product_id_parent_sequence_index" on "product_ingredient" ("parent_product_id", "parent_sequence");'
    )
