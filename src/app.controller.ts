import { EntityManager, QueryBuilder } from '@mikro-orm/postgresql';
import { Body, Controller, Get, Logger, Post, Query } from '@nestjs/common';
import { Product } from './domain/entities/product';
import { MongoClient } from 'mongodb';
import * as fs from 'fs';
import * as readline from 'readline';
import { Ulid } from 'id128';
import { TAG_MAPPINGS } from './domain/entities/product-tags';
import { EntityName } from '@mikro-orm/core';

@Controller()
export class AppController {
  private logger = new Logger(AppController.name);
  constructor(private em: EntityManager) { }

  // Lowish batch size seems to work best, probably due to the size of the product document
  importBatchSize = 100;
  importLogInterval = 1000;

  private tags = Object.keys(TAG_MAPPINGS);

  private fields = [
    'code',
    'product_name',
    'ingredients_text',
    'nutrition_data_per',
    'nutrition_data_prepared_per',
    'serving_quantity',
    'serving_size',
    'creator',
    'owners_tags',
    'last_modified_t',
  ];

  @Get('importfromfile?')
  async importFromFile(@Query('from') from = null) {
    const updateId = from ? Ulid.generate().toRaw() : null;
    const fromTime = from ? Math.floor(new Date(from).getTime() / 1000) : null;
    const rl = readline.createInterface({
      input: fs.createReadStream('data/openfoodfacts-products.jsonl'),
    });

    if (!from) await this.deleteAllProducts();
    //await this.cacheTags();
    let i = 0;
    let skip = 0;
    for await (const line of rl) {
      try {
        if (from) {
          const tIndex = line.indexOf('"last_modified_t":');
          if (tIndex > 0) {
            const lastModified = parseInt(
              line.substring(tIndex + 18, line.indexOf(',', tIndex)),
            );
            if (lastModified < fromTime) {
              skip++;
              if (!(skip % this.importLogInterval)) {
                this.logger.log(`Skippped ${skip}`);
              }
              continue;
            }
          }
        }

        const data = JSON.parse(line.replace(/\\u0000/g, ''));
        i++;
        await this.fixupProduct(updateId, data);
        if (!(i % this.importBatchSize)) {
          await this.em.flush();
          this.em.clear();
        }
        if (!(i % this.importLogInterval)) {
          this.logger.log(`Updated ${i}`);
        }
      } catch (e) {
        this.logger.log(e.message + ': ' + line);
      }
    }
    await this.em.flush();
    this.logger.log(`${i} Products imported`);
    await this.updateTags(updateId);
  }

  @Get('convertfiletocsv?')
  async convertFileToCsv() {
    const rl = readline.createInterface({
      input: fs.createReadStream('data/openfoodfacts-products.jsonl'),
    });

    const out = fs.openSync('data/product_tag.csv', 'w');
    //await this.cacheTags();
    let i = 0;
    for await (const line of rl) {
      try {
        i++;
        const data = JSON.parse(line.replace(/\\u0000/g, ''));
        const id = Ulid.generate().toRaw();
        for (const key of this.tags) {
          for (const [index, value] of Object.entries(data[key] || [])) {
            fs.appendFileSync(out, `${id},${key},${index},${value}\n`);
          }
        }
        if (data.creator)
          fs.appendFileSync(out, `${id},creator,0,${data.creator}\n`);

        if (data.owners_tags)
          fs.appendFileSync(out, `${id},owners_tags,0,${data.owners_tags}\n`);

        if (!(i % this.importLogInterval)) {
          this.logger.log(i);
        }
      } catch (e) {
        this.logger.error(line, e);
      }
    }
    fs.closeSync(out);
    this.logger.log(i);
  }

  @Get('importfrommongo?')
  async importFromMongo(@Query('from') from = null) {
    const filter = {};
    if (from) {
      const fromTime = Math.floor(new Date(from).getTime() / 1000);
      filter['last_modified_t'] = { $gt: fromTime };
    }
    const updateId = from ? Ulid.generate().toRaw() : null;
    if (!from) await this.deleteAllProducts();
    //await this.cacheTags();
    this.logger.log('Connecting to MongoDB');
    const client = new MongoClient('mongodb://127.0.0.1:27017');
    await client.connect();
    const db = client.db('off');
    const products = db.collection('products');
    const projection = {};
    for (const key of this.fields) {
      projection[key] = 1;
    }
    for (const key of this.tags) {
      projection[key] = 1;
    }
    const cursor = products.find(filter, { projection });
    let i = 0;
    this.logger.log('Starting import');
    while (true) {
      const data = await cursor.next();
      if (!data) break;

      i++;
      await this.fixupProduct(updateId, data);
      if (!(i % this.importBatchSize)) {
        await this.em.flush();
        this.em.clear();
      }
      if (!(i % this.importLogInterval)) {
        this.logger.log(i);
      }
    }
    //await this.em.getConnection().execute('commit');
    await this.em.flush();
    this.logger.log(`${i} Products imported`);
    await cursor.close();
    await client.close();
    await this.updateTags(updateId);
  }

  @Post('query')
  async query(@Body() body: any) {
    const start = Date.now();
    this.logger.log(body);

    const match = body.find((o: any) => o['$match'])?.['$match'];
    const group = body.find((o: any) => o['$group'])?.['$group'];

    const tag = group['_id'].substring(1);
    const { entity, column } = this.getEntityAndColumn(tag);
    const qb = this.em
      .createQueryBuilder(entity, 'pt')
      .select(`${column} _id, count(*) count`);

    const matchTag = Object.keys(match)[0];
    let matchValue = Object.values(match)[0];
    const not = matchValue?.['$ne'];
    if (matchTag) {
      if (not) {
        matchValue = not;
      }
      const { entity: matchEntity, column: matchColumn } =
        this.getEntityAndColumn(matchTag);
      const qbWhere = this.em
        .createQueryBuilder(matchEntity, 'pt2')
        .select('*')
        .where(`pt2.product_id = pt.product_id and pt2.${matchColumn} = ?`, [
          matchValue,
        ]);
      qb.where(`${not ? 'NOT ' : ''}EXISTS (${qbWhere.getKnexQuery()})`);
    }
    qb.groupBy(column)
      .orderBy({ ['2']: 'DESC' })
      .limit(10000);

    const results = await qb.execute();
    //this.logger.log(results);
    this.logger.log(
      `Processed ${tag}${matchTag ? ` where ${matchTag} ${not ? '!=' : '=='} ${matchValue}` : ''
      } in ${Date.now() - start} ms. Returning ${results.length} records`,
    );
    return results;
  }

  private getEntityAndColumn(tag: any) {
    let entity: EntityName<object>;
    let column = 'value';
    if (this.fields.includes(tag)) {
      entity = Product;
      column = tag;
    } else {
      entity = TAG_MAPPINGS[tag];
    }
    return { entity, column };
  }

  private async updateTags(updateId: string) {
    const connection = this.em.getConnection();
    for (const [tag, entity] of Object.entries(TAG_MAPPINGS)) {
      let logText = `Updated ${tag}`;
      const tableName = this.em.getMetadata(entity).tableName;
      if (updateId) {
        const results = await connection.execute(
          `delete from off.${tableName} 
        where product_id in (select id from off.product 
        where last_update_id = ?)`,
          [updateId],
          'run',
        );
        logText += ` deleted ${results['affectedRows']},`;
      }
      const results = await connection.execute(
        `insert into off.${tableName} (product_id, sequence, value)
        select id, tag.ordinality, tag.value from off.product 
        cross join jsonb_array_elements_text(data->'${tag}') with ordinality tag
        ${updateId ? `where last_update_id = ?` : ''}`,
        [updateId],
        'run',
      );
      logText += ` inserted ${results['affectedRows']} rows`;
      this.logger.log(logText);
    }
    await connection.execute('commit');
    this.logger.log('Finished');
  }

  private async findOrNewProduct(updateId: string, data: any) {
    let product: Product;
    if (updateId) {
      const code = data.code;
      if (code) product = await this.em.findOne(Product, { code: code });
    }
    if (!product) {
      product = new Product();
      this.em.persist(product);
    }
    return product;
  }

  async deleteAllProducts() {
    await this.em.execute('truncate table off.product cascade');
    // for (const entity of Object.values(TAG_MAPPINGS)) {
    //   await this.deleteAndFlush(entity);
    // }
    // await this.deleteAndFlush(Product);
  }

  async deleteAndFlush(entityName: { new(...args: any): object }) {
    this.logger.log('Deleting ' + entityName.name);
    await this.em.nativeDelete(entityName, {});
    await this.em.flush();
  }

  async deleteProductChildren(product: Product) {
    for (const entity of Object.values(TAG_MAPPINGS)) {
      await this.em.nativeDelete(entity, { product: product });
    }
  }

  async fixupProduct(updateId: string, data: any): Promise<void> {
    const product = await this.findOrNewProduct(updateId, data);
    const dataToStore = {};
    for (const key of this.tags) {
      dataToStore[key] = data[key];
    }
    product.data = dataToStore;
    product.name = data.product_name;
    product.code = data.code;
    product.creator = data.creator;
    product.ownersTags = data.owners_tags;
    product.ingredientsText = data.ingredients_text;
    product.nutritionAsSoldPer = data.nutrition_data_per;
    product.nutritionPreparedPer = data.nutrition_data_prepared_per;
    product.servingQuantity = data.serving_quantity;
    product.servingSize = data.serving_size;
    try {
      product.lastModified = new Date(data.last_modified_t * 1000);
    } catch (e) {
      this.logger.log(`${e.message}: ${data.last_modified_t}.`);
    }
    product.lastUpdateId = updateId;
    //this.importTags(product, data);
  }

  importTags(product: Product, data: any) {
    for (const [tag, entity] of Object.entries(TAG_MAPPINGS)) {
      const tags = data[tag] ?? [];
      for (const [sequence, value] of tags.entries()) {
        this.em.persist(new entity(product, sequence, value));
      }
    }
  }
  /*
  importIngredients(product: Product, sequence: number, ingredients: any[], parent?: ProductIngredient) {
    for (const offIngredient of ingredients ?? []) {
      const ingredient = this.em.create(ProductIngredient, {
        product: product,
        sequence: sequence++,
        id: offIngredient.id,
        ingredientText: offIngredient.text,
        percentMin: offIngredient.percent_min,
        percentMax: offIngredient.percent_max,
        percentEstimate: offIngredient.percent_estimate,
        parent: parent,
        ingredient: this.cachedTags['ingredients'].find((tag) => tag.id === offIngredient.id)
      });
      this.em.persist(ingredient);
      if (offIngredient.ingredients) {
        sequence = this.importIngredients(product, sequence, offIngredient.ingredients, ingredient);
      }
    }
    return sequence;
  }

  importNutrients(product: Product, nurientData: { [key: string]: any }) {
    const nutrients: { [key: string]: ProductNutrient } = {};
    for (const [key, value] of Object.entries(nurientData || {})) {
      const parts = key.split('_');
      const nutrientId = parts[0];
      const nutrient = nutrients[nutrientId]
        ??= new ProductNutrient(product, nutrientId, this.cachedTags['nutrients'].find((tag) => tag.id === 'zz:' + nutrientId));
      this.em.persist(nutrient);

      const prepared = (parts[1] === 'prepared');
      const suffix = prepared ? parts[2] : parts[1];
      if (suffix === 'unit')
        nutrient.enteredUnit = value;
      else if (suffix === 'modifier')
        if (prepared) nutrient.modifierPrepared = value;
        else nutrient.modifierAsSold = value;
      else if (suffix === 'label')
        nutrient.enteredName = value;
      else if (suffix === 'value')
        if (prepared) nutrient.enteredQuantityPrepared = value; //TODO: Need to make sure values are valid numbers
        else nutrient.enteredQuantityAsSold = value;
      else if (suffix === '100g')
        if (prepared) nutrient.quantityPer100gPrepared = value;
        else nutrient.quantityPer100gAsSold = value;
      else if (suffix === 'serving')
        if (prepared) nutrient.quantityPerServingPrepared = value;
        else nutrient.quantityPerServingAsSold = value;
      else
        if (prepared) nutrient.normalisedQuantityPrepared = value;
        else nutrient.normalisedQuantityAsSold = value;
    }
  }
  */
}
