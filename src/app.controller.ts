import { EntityManager } from '@mikro-orm/postgresql';
import { Body, Controller, Get, Logger, Post, Query } from '@nestjs/common';
import { Product } from './domain/entities/product';
import { ProductTag } from './domain/entities/product-tag';
import { MongoClient } from 'mongodb';
import * as fs from 'fs';
import * as readline from 'readline';
import { Ulid } from 'id128';

@Controller()
export class AppController {
  private logger = new Logger(AppController.name);
  constructor(private em: EntityManager) { }

  // Lowish batch size seems to work best, probably due to the size of the product document
  importBatchSize = 100;
  importLogInterval = 1000;

  private tags = [
    //'creator',
    'countries_tags',
    'brands_tags',
    'categories_tags',
    'labels_tags',
    'packaging_tags',
    'origins_tags',
    'manufacturing_places_tags',
    'emb_codes_tags',
    'ingredients_tags',
    'additives_tags',
    'vitamins_tags',
    'minerals_tags',
    'amino_acids_tags',
    'nucleotides_tags',
    'allergens_tags',
    'traces_tags',
    'nova_groups_tags',
    'nutrition_grades_tags',
    'languages_tags',
    'creator_tags',
    'editors_tags',
    'states_tags',
    'entry_dates_tags',
    'last_edit_dates_tags',
    'codes_tags',
    'nutrient_levels_tags',
    'stores_tags',
    'informers_tags',
    'photographers_tags',
    'checkers_tags',
    'correctors_tags',
    'ingredients_from_palm_oil_tags',
    'ingredients_that_may_be_from_palm_oil_tags',
    'purchase_places_tags',
    'ingredients_n_tags',
    'pnns_groups_1_tags',
    'pnns_groups_2_tags',
    'misc_tags',
    'quality_tags',
    'unknown_nutrients_tags',
    'last_image_dates_tags',
    'cities_tags',
    'ingredients_analysis_tags',
    'popularity_tags',
    'data_sources_tags',
    'data_quality_tags',
    'data_quality_bugs_tags',
    'data_quality_info_tags',
    'data_quality_warnings_tags',
    'data_quality_errors_tags',
    'teams_tags',
    'categories_properties_tags',
    'ecoscore_tags',
    //'owners_tags',
    'food_groups_tags',
    'weighers_tags',
  ];

  private fields = [
    'code',
    'product_name',
    'ingredients_text',
    'nutrition_data_per',
    'nutrition_data_prepared_per',
    'serving_quantity',
    'serving_size',
    'creator',
    'ownders_tags',
    'last_modified_t',
  ];

  @Get('importfromfile?')
  async importFromFile(@Query('update') update = false) {
    const rl = readline.createInterface({
      input: fs.createReadStream('data/openfoodfacts-products.jsonl'),
    });

    await this.deleteProducts(update);
    //await this.cacheTags();
    let i = 0;
    for await (const line of rl) {
      try {
        i++;
        const data = JSON.parse(line.replace(/\\u0000/g, ''));
        await this.fixupProduct(update, data);
        if (!(i % this.importBatchSize)) {
          await this.em.flush();
          this.em.clear();
        }
        if (!(i % this.importLogInterval)) {
          this.logger.log(i);
        }
      } catch (e) {
        this.logger.log(e.message + ': ' + line);
      }
    }
    await this.em.flush();
    this.logger.log(i);
    await this.evaluateTags();
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
        this.logger.log(e.message + ': ' + line);
      }
    }
    fs.closeSync(out);
    this.logger.log(i);
  }

  @Get('importfrommongo?')
  async importFromMongo(@Query('update') update = false) {
    await this.deleteProducts(update);
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
    const cursor = products.find({}, { projection });
    let i = 0;
    this.logger.log('Starting import');
    while (true) {
      const data = await cursor.next();
      if (!data) break;

      i++;
      await this.fixupProduct(update, data);
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
    this.logger.log(i);
    await cursor.close();
    await client.close();
    await this.evaluateTags();
  }

  @Post('query')
  async query(@Body() body: any) {
    this.logger.log(body);

    const match = body.find((o: any) => o['$match']);
    const group = body.find((o: any) => o['$group']);

    const tag = group['$group']['_id'].substring(1);
    const qb = this.em
      .createQueryBuilder(ProductTag, 'pt')
      .select('value _id, count(*) count')
      .where({ 'pt.tag_type': tag })
      .groupBy('value')
      .orderBy({ ['1']: 'ASC' });

    const results = await qb.execute();
    this.logger.log(results);
    return results;
    return [
      { _id: 'unknown', count: 200 },
      { _id: 'd', count: 20 },
      { _id: 'b', count: 10 },
      { _id: 'c', count: 90 },
      { _id: 'e', count: 70 },
      { _id: 'not-applicable', count: 40 },
    ];
  }

  private async evaluateTags() {
    const connection = this.em.getConnection();
    for (const tag of this.tags) {
      this.logger.log(tag);
      await connection.execute(
        `insert into off.product_tag (product_id, sequence, tag_type, value)
        select id, tag.ordinality, '${tag}', tag.value from off.product 
        cross join jsonb_array_elements_text(data->'${tag}') with ordinality tag`,
      );
      await connection.execute('commit');
    }
    this.logger.log('Finished');
  }

  private async findOrNewProduct(update: boolean, data: any) {
    let product: Product;
    if (update) {
      const code = data.code;
      if (code) product = await this.em.findOne(Product, { code: code });
    }
    if (!product) {
      product = new Product();
      this.em.persist(product);
    }
    return product;
  }

  async deleteProducts(update) {
    await this.deleteProductChildren();
    if (!update) {
      await this.deleteAndFlush(Product);
    }
  }

  async deleteProductChildren() {
    const connection = this.em.getConnection();
    await connection.execute('truncate off.product_tag');
    await connection.execute('commit');
    //deleteAndFlush(ProductTag);
    //await this.deleteAndFlush(ProductIngredient);
    //await this.deleteAndFlush(ProductNutrient);
  }

  async deleteAndFlush(entityName: { new(...args: any): object }) {
    this.logger.log('Deleting ' + entityName.name);
    await this.em.nativeDelete(entityName, {});
    await this.em.flush();
  }

  async fixupProduct(update: boolean, data: any): Promise<void> {
    const product = await this.findOrNewProduct(update, data);
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
    product.lastModified = new Date(data.last_modified_t * 1000);
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
