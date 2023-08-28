import { Injectable, Logger } from '@nestjs/common';
import { MAPPED_FIELDS, Product } from '../entities/product';
import { Ulid } from 'id128';
import { MongoClient } from 'mongodb';
import { EntityManager } from '@mikro-orm/postgresql';
import { MAPPED_TAGS } from '../entities/product-tags';
import * as fs from 'fs';
import * as readline from 'readline';

@Injectable()
export class ImportService {
  private logger = new Logger(ImportService.name);

  constructor(private em: EntityManager) {}

  // Lowish batch size seems to work best, probably due to the size of the product document
  importBatchSize = 100;
  importLogInterval = 1000;

  private tags = Object.keys(MAPPED_TAGS);

  async importFromMongo(from?: string, skip?: number) {
    if (!from && from != null) {
      const result = await this.em
        .createQueryBuilder(Product, 'p')
        .select(['max(p.last_modified) modified'])
        .execute();
      from = result?.[0]?.['modified'];
    }
    const filter = {};
    if (from) {
      const fromTime = Math.floor(new Date(from).getTime() / 1000);
      filter['last_modified_t'] = { $gt: fromTime };
    }
    const updateId = Ulid.generate().toRaw();
    if (!from) await this.deleteAllProducts();

    this.logger.log('Connecting to MongoDB');
    const client = new MongoClient(
      `mongodb://${process.env['MONGODB_HOST']}:27017`,
    );
    await client.connect();
    const db = client.db('off');
    const projection = {};
    for (const key of MAPPED_FIELDS) {
      projection[key] = 1;
    }
    for (const key of this.tags) {
      projection[key] = 1;
    }
    this.logger.log('Starting import' + (from ? ' from ' + from : ''));
    for (const obsolete of [false, true]) {
      const products = db.collection(`products${obsolete ? '_obsolete' : ''}`);
      const cursor = products.find(filter, { projection });
      let i = 0;
      while (true) {
        const data = await cursor.next();
        if (!data) break;

        i++;
        if (skip && i < skip) continue;
        await this.fixupProduct(!!from, updateId, data, obsolete);
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
    }
    await this.updateTags(!!from, updateId);
    await client.close();
    this.logger.log('Finished');
  }

  async fixupProduct(
    update: boolean,
    updateId: string,
    data: any,
    obsolete = false,
  ): Promise<void> {
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
    product.obsolete = obsolete;
    const lastModified = new Date(data.last_modified_t * 1000);
    if (isNaN(+lastModified)) {
      this.logger.log(`Invalid last_modified_t: ${data.last_modified_t}.`);
    } else {
      product.lastModified = lastModified;
    }
    product.lastUpdateId = updateId;
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

  private async updateTags(update: boolean, updateId: string) {
    const connection = this.em.getConnection();
    for (const [tag, entity] of Object.entries(MAPPED_TAGS)) {
      let logText = `Updated ${tag}`;
      const tableName = this.em.getMetadata(entity).tableName;
      if (update) {
        const results = await connection.execute(
          `delete from ${tableName} 
        where product_id in (select id from product 
        where last_update_id = ?)`,
          [updateId],
          'run',
        );
        logText += ` deleted ${results['affectedRows']},`;
      }
      const results = await connection.execute(
        `insert into ${tableName} (product_id, value, obsolete)
        select DISTINCT id, tag.value, obsolete from product 
        cross join jsonb_array_elements_text(data->'${tag}') tag
        ${updateId ? `WHERE last_update_id = ?` : ''}`,
        [updateId],
        'run',
      );
      await connection.execute('commit');
      logText += ` inserted ${results['affectedRows']} rows`;
      this.logger.log(logText);
    }
  }

  async deleteAllProducts() {
    await this.em.execute('truncate table product cascade');
  }

  async importFromFile(from = null) {
    const updateId = Ulid.generate().toRaw();
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
        await this.fixupProduct(!!from, updateId, data);
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
    await this.updateTags(!!from, updateId);
  }
}
