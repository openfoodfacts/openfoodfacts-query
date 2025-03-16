from typing import Dict, List
from query.models.product import Product


async def create_table(connection):
    await connection.execute(
        """create table product_ingredient (
            product_id int not null,
            sequence text not null,
            parent_product_id int null,
            parent_sequence text null,
            ingredient_text text null,
            id text null,
            ciqual_food_code text null,
            percent_min double precision null,
            percent text null,
            percent_max double precision null,
            percent_estimate double precision null,
            data json null,
            obsolete boolean null default false,
            constraint product_ingredient_pkey primary key (product_id, sequence))""",
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


async def get_ingredients(connection, product_id):
    return await connection.fetch(f"SELECT * FROM product_ingredient WHERE product_id = $1", product_id)


async def create_ingredients(connection, product: Product, ingredients: List[Dict], parent_sequence = None):
    # TODO: Test extra fields
    if parent_sequence == None:
        await connection.execute("DELETE FROM product_ingredient WHERE product_id = $1", product.id)

    for seq, ingredient in enumerate(ingredients):
        sequence = str(seq + 1) if parent_sequence == None else parent_sequence + '.' + (seq + 1)
        await connection.execute("""INSERT INTO product_ingredient (product_id, sequence, parent_sequence, ingredient_text) VALUES ($1, $2, $3, $4)""",
                                 product.id, sequence, parent_sequence, ingredient['ingredient_text'])
        if 'ingredients' in ingredient:
            await create_ingredients(connection, product, ingredient['ingredients'], sequence)
            

async def delete_ingredients(connection, product_ids):
    await connection.execute(f"UPDATE product_ingredient SET obsolete = NULL WHERE product_id = ANY($1::int[])", product_ids)
  
