async def create_table(connection):
    await connection.execute(
        'create table product_ingredient (product_id uuid not null, sequence text not null, parent_product_id uuid null, parent_sequence text null, ingredient_text text null, id text null, ciqual_food_code text null, percent_min double precision null, percent text null, percent_max double precision null, percent_estimate double precision null, data json null, obsolete boolean null default false, constraint product_ingredient_pkey primary key (product_id, sequence));',
    )
    await connection.execute(
        'create index product_ingredient_parent_product_id_parent_sequence_index on product_ingredient (parent_product_id, parent_sequence);',
    )

    await connection.execute(
        'alter table product_ingredient add constraint product_ingredient_product_id_foreign foreign key (product_id) references product (id) on update cascade on delete cascade;',
    )
    await connection.execute(
        'alter table product_ingredient add constraint product_ingredient_parent_product_id_parent_sequence_foreign foreign key (parent_product_id, parent_sequence) references product_ingredient (product_id, sequence) on update cascade on delete set null;',
    )


async def drop_old_id(connection):
    await connection.execute(
        "alter table query.product_ingredient DROP CONSTRAINT product_ingredient_pkey CASCADE;"
    )
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

async def populate_new_product_id(connection):
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

    await connection.execute(
        'create index "product_ingredient_parent_product_id_parent_sequence_index" on "product_ingredient" ("parent_product_id", "parent_sequence");'
    )
