import { Injectable, Logger } from '@nestjs/common';
import { MAPPED_FIELDS, Product } from '../entities/product';
import { Ulid } from 'id128';
import { MongoClient } from 'mongodb';
import { EntityManager } from '@mikro-orm/postgresql';
import * as fs from 'fs';
import * as readline from 'readline';
import { TagService } from './tag.service';
import { ProductTagMap } from '../entities/product-tag-map';
import { createClient, commandOptions } from 'redis';
import { ProductSource } from '../enums/product-source';
import equal from 'fast-deep-equal';

@Injectable()
export class ImportService {
  private logger = new Logger(ImportService.name);
  private client: any; // Don't strongly type here is it is really verbose
  private lastMessageId: string;

  constructor(
    private readonly em: EntityManager,
    private readonly tagService: TagService,
  ) {}

  // Lowish batch size seems to work best, probably due to the size of the product document
  importBatchSize = 100;
  importLogInterval = 1000;

  private tags = Object.keys(ProductTagMap.MAPPED_TAGS);

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
      this.logger.log(`Starting import from ${from}`);
    }

    await this.importWithFilter(
      filter,
      from ? ProductSource.INCREMENTAL_LOAD : ProductSource.FULL_LOAD,
      skip,
    );
  }

  async importWithFilter(filter: any, source: ProductSource, skip?: number) {
    const fullImport = !Object.keys(filter).length;

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
        await this.fixupProduct(updateId, data, obsolete, source);
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
    await this.updateTags(updateId, fullImport);

    // If doing a full import delete all products that weren't updated
    if (fullImport) {
      await this.deleteOtherProducts(updateId);
    }
    this.logger.log('Finished');
  }

  /** Populate a Product record from MongoDB document */
  nulRegex = /\0/g;
  async fixupProduct(
    updateId: string,
    data: any,
    obsolete = false,
    source: ProductSource,
  ): Promise<void> {
    const product = await this.findOrNewProduct(data);
    // Skip products that don't have a code
    if (!product) return;

    for (const key of this.tags) {
      const tagData = data[key] as string[];
      if (tagData) {
        // Strip out any nul characters
        for (const [index, value] of tagData.entries()) {
          if (value.includes('\u0000')) {
            this.logger.warn(
              `Product: ${data.code}. Nuls stripped from ${key} value: ${value}`,
            );
            tagData[index] = value.replace(this.nulRegex, '');
          }
        }
      }
    }
    if (product.data && product.data.last_modified_t === data.last_modified_t) {
      // If last modified data is not changed the product probably hasn't changed
      // But compare data anyway just in case
      if (equal(product.data, data)) return;
    }

    product.data = data;
    product.name = data.product_name;
    product.code = data.code;
    product.creator = data.creator;
    product.ownersTags = data.owners_tags;
    product.obsolete = obsolete;
    product.ingredientsCount = data.ingredients_n;
    product.ingredientsWithoutCiqualCodesCount =
      data.ingredients_without_ciqual_codes_n;
    const lastModified = new Date(data.last_modified_t * 1000);
    if (isNaN(+lastModified)) {
      this.logger.warn(
        `Product: ${data.code}. Invalid last_modified_t: ${data.last_modified_t}.`,
      );
    } else {
      product.lastModified = lastModified;
    }
    product.lastUpdateId = updateId;
    product.lastUpdated = new Date();
    product.source = source;
    //await this.em.nativeDelete(ProductIngredient, { product: product });
    //this.importIngredients(product, 0, data.ingredients);
  }

  /** Find an existing document by product code, or create a new one */
  private async findOrNewProduct(data: any) {
    let product: Product;
    const code = data.code;
    if (code == null) return null;
    product = await this.em.findOne(Product, { code: code });
    if (!product) {
      product = new Product();
      this.em.persist(product);
    }
    return product;
  }

  /**
   * Products are first loaded with the tags in the data JSON property.
   * SQL is then run to insert this into the individual tag tables.
   * This was found to be quicker than using ORM functionality
   */
  async updateTags(updateId: string, fullImport = false) {
    this.logger.log(`Updating tags for updateId: ${updateId}`);

    const connection = this.em.getConnection();

    // Fix ingredients
    let logText = `Updated ingredients`;
    await connection.execute('begin');
    const deleted = await connection.execute(
      `delete from product_ingredient 
    where product_id in (select id from product 
    where last_update_id = ?)`,
      [updateId],
      'run',
    );
    logText += ` deleted ${deleted['affectedRows']},`;
    const results = await connection.execute(
      `insert into product_ingredient (
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
        tag.value->>'ingredient_text',
        tag.value->>'percent',
        (tag.value->>'percent_min')::numeric,
        (tag.value->>'percent_max')::numeric,
        (tag.value->>'percent_estimate')::numeric,
        tag.value->'ingredients',
        product.obsolete
      from product 
      cross join json_array_elements(data->'ingredients') with ordinality tag
      WHERE last_update_id = ?`,
      [updateId],
      'run',
    );
    let affectedRows = results['affectedRows'];
    logText += ` inserted ${affectedRows}`;
    while (affectedRows > 0) {
      const results = await connection.execute(
        `insert into product_ingredient (
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
          tag.value->>'ingredient_text',
          tag.value->>'percent',
          (tag.value->>'percent_min')::numeric,
          (tag.value->>'percent_max')::numeric,
          (tag.value->>'percent_estimate')::numeric,
          tag.value->'ingredients',
          pi.obsolete
        from product_ingredient pi 
        join product on product.id = pi.product_id
        cross join json_array_elements(pi.data) with ordinality tag
        WHERE pi.data IS NOT NULL
        AND NOT EXISTS (SELECT * FROM product_ingredient pi2 WHERE pi2.parent_product_id = pi.product_id AND pi2.parent_sequence = pi.sequence)
        AND product.last_update_id = ?`,
        [updateId],
        'run',
      );
      affectedRows = results['affectedRows'];
      logText += ` > ${affectedRows}`;
    }
    await connection.execute('commit');
    this.logger.log(logText + ' rows');

    for (const [tag, entity] of Object.entries(ProductTagMap.MAPPED_TAGS)) {
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
        cross join json_array_elements_text(data->'${tag}') tag
        WHERE last_update_id = ?`,
        [updateId],
        'run',
      );

      // Commit after each tag to minimise server snapshot size
      await connection.execute('commit');

      // If this is a full load we can flag the tag as now available for query
      if (fullImport) {
        await this.tagService.tagLoaded(tag);
      }

      logText += ` inserted ${results['affectedRows']} rows`;

      this.logger.log(logText);
    }
  }

  async deleteOtherProducts(updateId: string) {
    const deleted = await this.em.nativeDelete(Product, {
      $or: [{ lastUpdateId: { $ne: updateId } }, { lastUpdateId: null }],
    });
    this.logger.log(`${deleted} Products deleted`);
  }

  async startRedisConsumer() {
    const redisUrl = process.env['REDIS_URL'];
    if (!redisUrl) return;
    this.lastMessageId = '$';
    this.client = createClient({ url: redisUrl });
    this.client.on('error', (err) => this.logger.error(err));
    await this.client.connect();
    this.receiveMessages();
  }

  receiveMessages() {
    const self = this;
    this.client
      .xRead(
        commandOptions({
          isolated: true,
        }),
        [
          // XREAD can read from multiple streams, starting at a
          // different ID for each...
          {
            key: 'product_update',
            id: self.lastMessageId,
          },
        ],
        {
          // Read 1000 entry at a time, block for 5 seconds if there are none.
          COUNT: 1000,
          BLOCK: 5000,
        },
      )
      .then(async (keys) => {
        if (keys?.length) {
          const messages = keys[0].messages;
          if (messages?.length) {
            const productCodes = messages.map((m) => m.message.code);
            const filter = { code: { $in: productCodes } };
            await this.importWithFilter(filter, ProductSource.EVENT);
            this.lastMessageId = messages[messages.length - 1].id;
          }
        }
        setTimeout(() => {
          this.receiveMessages();
        }, 0);
      });
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
        await this.fixupProduct(
          updateId,
          data,
          false,
          from ? ProductSource.INCREMENTAL_LOAD : ProductSource.FULL_LOAD,
        );
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
    await this.updateTags(updateId, !from);
    if (!from) {
      await this.deleteOtherProducts(updateId);
    }
    this.logger.log('Finished');
  }
}
