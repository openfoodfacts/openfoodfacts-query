import { EntityManager } from '@mikro-orm/core';
import { Controller, Get, Logger, Query } from '@nestjs/common';
import { Product } from './domain/entities/product';
import { ProductTag } from './domain/entities/product-tag';
import { MongoClient } from 'mongodb';
import * as fs from 'fs';
import * as readline from 'readline';

@Controller()
export class AppController {
  private logger = new Logger(AppController.name);
  constructor(private em: EntityManager) {}

  // Lowish batch size seems to work best, probably due to the size of the product document
  importBatchSize = 300;
  importLogInterval = 1000;

  @Get('importfromfile?')
  async importFromFile(@Query('update') update = false) {
    const rl = readline.createInterface({
      input: fs.createReadStream('jsonl/openfoodfacts-products.jsonl'),
    });

    await this.deleteProducts(update);
    //await this.cacheTags();
    const start = new Date().getTime();
    let i = 0;
    for await (const line of rl) {
      try {
        i++;
        const data = JSON.parse(line.replace(/\\u0000/g, ''));

        this.em.persist(await this.fixupProduct(update, data));
        if (!(i % this.importBatchSize)) {
          await this.em.flush();
          this.em.clear();
        }
        if (!(i % this.importLogInterval)) {
          this.logger.log(new Date().getTime() - start + ': ' + i);
        }
      } catch (e) {
        this.logger.log(e.message + ': ' + line);
      }
    }
    await this.em.flush();
    this.logger.log(new Date().getTime() - start + ': ' + i);
  }

  @Get('importfrommongo?')
  async importFromMongo(@Query('update') update = false) {
    const start = new Date().getTime();
    await this.deleteProducts(update);
    //await this.cacheTags();
    this.logger.log(new Date().getTime() - start + ': Connecting to MongoDB');
    const client = new MongoClient('mongodb://127.0.0.1:27017');
    await client.connect();
    const db = client.db('off');
    const products = db.collection('products');
    const cursor =
      products.find(/*{}, {
      projection: {
        code: 1,
        data_quality_tags: 1,
        additives_tags: 1,
        allergens_hierarchy: 1,
        states_tags: 1,
        categories_tags: 1,
        countries_hierarchy: 1,
        misc_tags: 1
      }
    }*/);
    let i = 0;
    this.logger.log(new Date().getTime() - start + ': Starting import');
    while (true) {
      const data = await cursor.next();
      if (!data) break;

      this.em.persist(await this.fixupProduct(update, data));
      if (!(++i % this.importBatchSize)) {
        await this.em.flush();
        this.em.clear();
      }
      if (!(i % this.importLogInterval)) {
        this.logger.log(new Date().getTime() - start + ': ' + i);
      }
    }
    await this.em.flush();
    this.logger.log(new Date().getTime() - start + ': ' + i);
    await cursor.close();
    await client.close();
  }

  private async findOrNewProduct(update: boolean, data: any) {
    let product: Product;
    if (update) {
      const code = data.code;
      if (code) product = await this.em.findOne(Product, { code: code });
    }
    if (!product) product = new Product();
    return product;
  }

  async deleteProducts(update) {
    if (!update) {
      await this.deleteProductChildren();
      await this.deleteAndFlush(Product);
    }
  }

  async deleteProductChildren() {
    await this.deleteAndFlush(ProductTag);
    //await this.deleteAndFlush(ProductIngredient);
    //await this.deleteAndFlush(ProductNutrient);
  }

  async deleteAndFlush(entityName: { new (...args: any): object }) {
    this.logger.log('Deleting ' + entityName.name);
    await this.em.nativeDelete(entityName, {});
    await this.em.flush();
  }

  async fixupProduct(update: boolean, data: any): Promise<Product> {
    const product = await this.findOrNewProduct(update, data);
    //product.data = data;

    product.name = data.product_name;
    product.code = data.code;
    product.ingredientsText = data.ingredients_text;
    product.NutritionAsSoldPer = data.nutrition_data_per;
    product.NutritionPreparedPer = data.nutrition_data_prepared_per;
    product.ServingQuantity = data.serving_quantity;
    product.ServingSize = data.serving_size;

    if (update) await this.em.nativeDelete(ProductTag, { product: product });
    this.importTags(
      data.data_quality_tags,
      product,
      'data_quality',
      'data_quality',
    );
    this.importTags(data.additives_tags, product, 'additives', 'ingredients');
    this.importTags(data.allergens_hierarchy, product, 'allergens', 'traces');
    this.importTags(data.states_tags, product, 'states', 'states');
    this.importTags(data.categories_tags, product, 'categories', 'categories');
    this.importTags(data.countries_hierarchy, product, 'countries', 'origins');
    this.importTags(data.misc_tags, product, 'misc', 'misc');
    /*
        await this.em.nativeDelete(ProductIngredient, { product: product });
        this.importIngredients(product, 0, data.ingredients);
    
        await this.em.nativeDelete(ProductNutrient, { product: product });
        this.importNutrients(product, data.nutriments);
    */
    return product;
  }

  private importTags(
    tagArray: any,
    product: Product,
    tagType: string,
    taxonomyGroup: string,
  ) {
    let i = 0;
    for (const value of tagArray ?? []) {
      this.em.persist(
        this.em.create(ProductTag, {
          product: product,
          sequence: i++,
          value: value,
          tagType: tagType,
          //tag: this.cachedTags[taxonomyGroup].find((tag) => tag.id === value)
        }),
      );
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
