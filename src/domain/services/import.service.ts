import { Injectable, Logger } from '@nestjs/common';
import { MAPPED_FIELDS, Product } from '../entities/product';
import { Ulid } from 'id128';
import { MongoClient } from 'mongodb';
import { EntityManager } from '@mikro-orm/postgresql';
import { MAPPED_TAGS } from '../entities/product-tags';
import * as fs from 'fs';
import * as readline from 'readline';
import { TagService } from './tag.service';

@Injectable()
export class ImportService {
  private logger = new Logger(ImportService.name);

  constructor(
    private readonly em: EntityManager,
    private readonly tagService: TagService,
  ) {}

  // Lowish batch size seems to work best, probably due to the size of the product document
  importBatchSize = 100;
  importLogInterval = 1000;

  private tags = Object.keys(MAPPED_TAGS);

  /** Import Products from MongoDB */
  async importFromMongo(from?: string, skip?: number) {
    // If the from parameter is supplied but it is empty then obtain the most
    // recent modified time from the database and query MongoDB for products
    // modified since then
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

    // The update id is unique to this run and is used later to run other
    // queries that should only affect products loaded in this import
    const updateId = Ulid.generate().toRaw();

    this.logger.log('Connecting to MongoDB');
    const client = new MongoClient(process.env.MONGO_URI);
    await client.connect();
    const db = client.db('off');

    // Only fetch the tags that we store to limit the payload from MongoDB
    const projection = {};
    for (const key of MAPPED_FIELDS) {
      projection[key] = 1;
    }
    for (const key of this.tags) {
      projection[key] = 1;
    }

    this.logger.log('Starting import' + (from ? ' from ' + from : ''));
    // Repeat the below for normal and then obsolete products
    // Both are stored in the same table in PostgreSQL
    for (const obsolete of [false, true]) {
      const products = db.collection(`products${obsolete ? '_obsolete' : ''}`);
      const cursor = products.find(filter, { projection });
      let i = 0;
      while (true) {
        const data = await cursor.next();
        if (!data) break;

        i++;
        if (skip && i < skip) continue;
        // Find the product if it exists and populate the standard fields
        await this.fixupProduct(true, updateId, data, obsolete);
        if (!(i % this.importBatchSize)) {
          // This will cause a commit and then clear the Mikro-ORM cache
          // to minimise memory consumption for large imports
          await this.em.flush();
          this.em.clear();
        }
        if (!(i % this.importLogInterval)) {
          this.logger.log(`Updated ${i}`);
        }
      }
      await this.em.flush();
      this.logger.log(`${i}${obsolete ? ' Obsolete' : ''} Products imported`);
      await cursor.close();
    }
    await client.close();

    // Tags are popualted using raw SQL from the data field
    await this.updateTags(!!from, updateId);

    // If doing a full import delete all products that weren't updated
    if (!from) {
      const deleted = await this.em.nativeDelete(Product, {
        $or: [{ lastUpdateId: { $ne: updateId } }, { lastUpdateId: null }],
      });
      this.logger.log(`${deleted} Products deleted`);
    }
    this.logger.log('Finished');
  }

  /** Populate a Product record from MongoDB document */
  nulRegex = /\0/g;
  async fixupProduct(
    update: boolean,
    updateId: string,
    data: any,
    obsolete = false,
  ): Promise<void> {
    const product = await this.findOrNewProduct(update, data);
    const dataToStore = {};
    for (const key of this.tags) {
      const tagData = data[key] as string[];
      if (tagData) {
        // Strip out any nul characters
        for (const [index, value] of tagData.entries()) {
          if (value.includes('\u0000')) {
            this.logger.warn(`Product: ${data.code}. Nuls stripped from ${key} value: ${value}`);
            tagData[index] = value.replace(this.nulRegex, '');
          }
        }
        dataToStore[key] = tagData;
      }
    }
    product.data = dataToStore;
    product.name = data.product_name;
    product.code = data.code;
    product.creator = data.creator;
    product.ownersTags = data.owners_tags;
    product.obsolete = obsolete;
    const lastModified = new Date(data.last_modified_t * 1000);
    if (isNaN(+lastModified)) {
      this.logger.warn(`Product: ${data.code}. Invalid last_modified_t: ${data.last_modified_t}.`);
    } else {
      product.lastModified = lastModified;
    }
    product.lastUpdateId = updateId;
  }

  /** Find an existing document by product code, or create a new one */
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

  /**
   * Products are first loaded with the tags in the data JSONB property.
   * SQL is then run to insert this into the individual tag tables.
   * This was found to be quicker than using ORM functionality
   */
  private async updateTags(update: boolean, updateId: string) {
    const connection = this.em.getConnection();
    for (const [tag, entity] of Object.entries(MAPPED_TAGS)) {
      let logText = `Updated ${tag}`;
      // Get the underlying table name for the entity
      const tableName = this.em.getMetadata(entity).tableName;

      await connection.execute('begin');

      // Delete existing tags for products that were imorted on this run
      const deleted = await connection.execute(
        `delete from ${tableName} 
      where product_id in (select id from product 
      where last_update_id = ?)`,
        [updateId],
        'run',
      );
      logText += ` deleted ${deleted['affectedRows']},`;

      // Add tags back in with the updated information
      const results = await connection.execute(
        `insert into ${tableName} (product_id, value, obsolete)
        select DISTINCT id, tag.value, obsolete from product 
        cross join jsonb_array_elements_text(data->'${tag}') tag
        ${updateId ? `WHERE last_update_id = ?` : ''}`,
        [updateId],
        'run',
      );

      // Commit after each tag to minimise server snapshot size
      await connection.execute('commit');

      // If this is a full load we can flag the tag as now available for query
      if (!update) {
        await this.tagService.tagLoaded(tag);
      }

      logText += ` inserted ${results['affectedRows']} rows`;

      this.logger.log(logText);
    }
  }

  async deleteAllProducts() {
    await this.em.execute('truncate table product cascade');
  }

  /**
   * Imports from a openfoodfacts-products.jsonl uploaded to the data folder
   * Mainly used for testing and may be removed.
   */
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
