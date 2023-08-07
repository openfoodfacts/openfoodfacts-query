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
    const projection = {};
    for (const key of this.fields) {
      projection[key] = 1;
    }
    for (const key of this.tags) {
      projection[key] = 1;
    }
    for (const obsolete of [false, true]) {
      const products = db.collection(`products${obsolete ? '_obsolete' : ''}`);
      const cursor = products.find(filter, { projection });
      let i = 0;
      this.logger.log('Starting import');
      while (true) {
        const data = await cursor.next();
        if (!data) break;

        i++;
        await this.fixupProduct(updateId, data, obsolete);
        if (!(i % this.importBatchSize)) {
          await this.em.flush();
          this.em.clear();
        }
        if (!(i % this.importLogInterval)) {
          this.logger.log(`Updated ${i}`);
        }
      }
      //await this.em.getConnection().execute('commit');
      await this.em.flush();
      this.logger.log(`${i}${obsolete ? ' Obsolete' : ''} Products imported`);
      await cursor.close();
      await this.updateTags(updateId, obsolete);
    }
    await client.close();
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
      .select(`${column} _id, count(*) count`)
      .where('not pt.obsolete');

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
      qb.andWhere(`${not ? 'NOT ' : ''}EXISTS (${qbWhere.getKnexQuery()})`);
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

  private async updateTags(updateId: string, obsolete = false) {
    const connection = this.em.getConnection();
    for (const [tag, entity] of Object.entries(TAG_MAPPINGS)) {
      let logText = `Updated ${tag}`;
      const tableName = this.em.getMetadata(entity).tableName;
      if (updateId) {
        const results = await connection.execute(
          `delete from off.${tableName} 
        where ${obsolete ? '' : 'NOT '}obsolete 
        AND product_id in (select id from off.product 
        where last_update_id = ?)`,
          [updateId],
          'run',
        );
        logText += ` deleted ${results['affectedRows']},`;
      }
      const results = await connection.execute(
        `insert into off.${tableName} (product_id, sequence, value, obsolete)
        select id, tag.ordinality, tag.value, ? from off.product 
        cross join jsonb_array_elements_text(data->'${tag}') with ordinality tag
        where ${obsolete ? '' : 'NOT '}obsolete
        ${updateId ? `AND last_update_id = ?` : ''}`,
        [obsolete, updateId],
        'run',
      );
      logText += ` inserted ${results['affectedRows']}${obsolete ? ' obsolete' : ''
        } rows`;
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
  }

  async fixupProduct(
    updateId: string,
    data: any,
    obsolete = false,
  ): Promise<void> {
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
    product.obsolete = obsolete;
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
}
