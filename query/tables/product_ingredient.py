from typing import Dict, List

from asyncpg import Connection
from query.database import get_rows_affected
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
        "create index product_ingredient_parent_product_id_parent_sequence_index on product_ingredient (parent_product_id, parent_sequence);",
    )
    await connection.execute(
        "alter table product_ingredient add constraint product_ingredient_product_id_foreign foreign key (product_id) references product (id) on update cascade on delete cascade;",
    )
    await connection.execute(
        "alter table product_ingredient add constraint product_ingredient_parent_product_id_parent_sequence_foreign foreign key (parent_product_id, parent_sequence) references product_ingredient (product_id, sequence) on update cascade on delete set null;",
    )


async def get_ingredients(connection, product_id):
    return await connection.fetch(
        f"SELECT * FROM product_ingredient WHERE product_id = $1", product_id
    )


def float_or_none(value):
    if value == None:
        return None
    return float(value)


async def create_ingredients(
    connection, product: Product, ingredients: List[Dict], parent_sequence=None
):
    # TODO: Test extra fields
    if parent_sequence == None:
        await connection.execute(
            "DELETE FROM product_ingredient WHERE product_id = $1", product.id
        )

    for seq, ingredient in enumerate(ingredients):
        sequence = (
            str(seq + 1)
            if parent_sequence == None
            else parent_sequence + "." + str(seq + 1)
        )
        await connection.execute(
            """INSERT INTO product_ingredient (
            product_id,
            sequence,
            parent_sequence,
            ingredient_text,
            id,
            ciqual_food_code,
            percent_min,
            percent,
            percent_max,
            percent_estimate
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)""",
            product.id,
            sequence,
            parent_sequence,
            ingredient.get("text"),
            ingredient.get("id"),
            ingredient.get("ciqual_food_code"),
            float_or_none(ingredient.get("percent_min")),
            str(ingredient.get("percent")),
            float_or_none(ingredient.get("percent_max")),
            float_or_none(ingredient.get("percent_estimate")),
        )
        if "ingredients" in ingredient:
            await create_ingredients(
                connection, product, ingredient["ingredients"], sequence
            )

async def create_ingredients_from_staging(connection: Connection, logger, obsolete):
      deleted = await connection.execute("""delete from product_ingredient 
        where product_id in (select id from product_temp)""")
      log_text = f"Updated ingredients deleted {get_rows_affected(deleted)},"
      results = await connection.execute(f"""insert into product_ingredient (
          product_id,
          sequence,
          id,
          ciqual_food_code,
          ingredient_text,
          percent,
          percent_min,
          percent_max,
          percent_estimate,
          data,
          obsolete
        )
        select 
          product.id,
          ordinality,
          tag.value->>'id',
          tag.value->>'ciqual_food_code',
          tag.value->>'text',
          tag.value->>'percent',
          (tag.value->>'percent_min')::numeric,
          (tag.value->>'percent_max')::numeric,
          (tag.value->>'percent_estimate')::numeric,
          tag.value->'ingredients',
          {obsolete}
        from product_temp product
        cross join jsonb_array_elements(data->'ingredients') with ordinality tag""")
      affected_rows = get_rows_affected(results)
      log_text += f" inserted {affected_rows}"
      while (affected_rows > 0):
        results = await connection.execute(f"""insert into product_ingredient (
            product_id,
            parent_product_id,
            parent_sequence,
            sequence,
            id,
            ciqual_food_code,
            ingredient_text,
            percent,
            percent_min,
            percent_max,
            percent_estimate,
            data,
            obsolete
          )
          select 
            pi.product_id,
            pi.product_id,
            pi.sequence,
            pi.sequence || '.' || ordinality,
            tag.value->>'id',
            tag.value->>'ciqual_food_code',
            tag.value->>'text',
            tag.value->>'percent',
            (tag.value->>'percent_min')::numeric,
            (tag.value->>'percent_max')::numeric,
            (tag.value->>'percent_estimate')::numeric,
            tag.value->'ingredients',
            {obsolete}
          from product_ingredient pi 
          join product_temp product on product.id = pi.product_id
          cross join json_array_elements(pi.data) with ordinality tag
          WHERE pi.data IS NOT NULL
          AND NOT EXISTS (SELECT * FROM product_ingredient pi2 WHERE pi2.parent_product_id = pi.product_id AND pi2.parent_sequence = pi.sequence)""")
        affected_rows = get_rows_affected(results)
        log_text += f" > {affected_rows}"
      logger.info(log_text)
    

async def delete_ingredients(connection, product_ids):
    await connection.execute(
        f"UPDATE product_ingredient SET obsolete = NULL WHERE product_id = ANY($1::int[])",
        product_ids,
    )
