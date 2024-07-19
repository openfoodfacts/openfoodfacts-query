import { Injectable, Logger } from '@nestjs/common';
import { MAPPED_FIELDS } from '../entities/product';
import { Ulid } from 'id128';
import { MongoClient } from 'mongodb';
import { EntityManager } from '@mikro-orm/postgresql';
import { TagService } from './tag.service';
import { ProductTagMap } from '../entities/product-tag-map';
import { createClient, commandOptions } from 'redis';
import { ProductSource } from '../enums/product-source';
import equal from 'fast-deep-equal';
import { SettingsService } from './settings.service';
import sql from '../../db';
import { ReservedSql } from 'postgres';
import { SerializableParameter } from 'postgres';
import { MessagesService } from './messages.service';

@Injectable()
export class ImportService {
  private logger = new Logger(ImportService.name);
  private client: any; // Don't strongly type here is it is really verbose

  constructor(
    private readonly em: EntityManager,
    private readonly tagService: TagService,
    private readonly settings: SettingsService,
    private readonly messages: MessagesService,
  ) {}

  // Lowish batch size seems to work best, probably due to the size of the product document
  importBatchSize = 10000;
  importLogInterval = 10000;
  importRunning = false;
  nulRegex = /\0/g;

  private tags = Object.keys(ProductTagMap.MAPPED_TAGS);

  /** Import Products from MongoDB */
  async importFromMongo(from?: string, skip?: number) {
    if (this.importRunning) {
      this.logger.warn('Skipping as import already running');
      return;
    }
    this.importRunning = true;
    try {
      // If the from parameter is supplied but it is empty then obtain the most
      // recent modified time from the database and query MongoDB for products
      // modified since then
      if (!from && from != null) {
        from = (await this.settings.getLastModified())?.toISOString();
      }
      const filter = {};
      if (from) {
        const fromTime = Math.floor(new Date(from).getTime() / 1000);
        filter['last_modified_t'] = { $gt: fromTime };
        this.logger.debug(`Starting import from ${from}`);
      }

      const latestModified = await this.importWithFilter(
        filter,
        from ? ProductSource.INCREMENTAL_LOAD : ProductSource.FULL_LOAD,
        skip,
      );
      if (latestModified) {
        await this.settings.setLastModified(new Date(latestModified));
      }
    } finally {
      this.importRunning = false;
    }
  }

  async importWithFilter(filter: any, source: ProductSource, skip?: number) {
    let latestModified = 0;

    // The update id is unique to this run and is used later to run other
    // queries that should only affect products loaded in this import
    const updateId = Ulid.generate().toRaw();

    this.logger.debug('Connecting to MongoDB');
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
    const collections = {
      normal: {
        obsolete: false,
        count: 0,
      },
      obsolete: {
        obsolete: true,
        count: 0,
      },
    };

    // Flush mikro-orm before switching to native SQL
    await this.em.flush();

    // Now using postgres to help with transactions
    const connection = await sql.reserve();
    await connection`CREATE TEMP TABLE product_temp (id int PRIMARY KEY, last_modified timestamptz, data jsonb)`;
    // let sql: string;
    // const vars = [];
    for (const collection of Object.values(collections)) {
      await connection`begin`;
      const obsolete = collection.obsolete;
      const products = db.collection(`products${obsolete ? '_obsolete' : ''}`);
      const cursor = products.find(filter, { projection });
      let i = 0;
      while (true) {
        const data = await cursor.next();
        if (!data) break;

        i++;
        if (skip && i < skip) continue;
        // Find the product if it exists
        let results =
          await connection`select id, last_modified from product where code = ${data.code}`;
        if (!results.length) {
          results =
            await connection`insert into product (code) values (${data.code}) returning id`;
        }
        const id = results[0].id;
        const previousLastModified = results[0].last_modified;

        let lastModified = new Date(data.last_modified_t * 1000);
        if (isNaN(+lastModified)) {
          this.logger.warn(
            `Product: ${data.code}. Invalid last_modified_t: ${data.last_modified_t}.`,
          );
          lastModified = null;
        }
        // Skip product if nothing has changed and not doing a full load
        if (
          source !== ProductSource.FULL_LOAD &&
          lastModified?.getTime() === previousLastModified?.getTime()
        )
          continue;

        for (const key of this.tags) {
          const tagData = data[key] as string[];
          if (tagData) {
            // Strip out any nul characters
            try {
              for (const [index, value] of tagData.entries()) {
                if (value.includes('\u0000')) {
                  this.logger.warn(
                    `Product: ${data.code}. Nuls stripped from ${key} value: ${value}`,
                  );
                  tagData[index] = value.replace(this.nulRegex, '');
                }
              }
            } catch (e) {
              this.logger.error(`${key}: ${e.message}`);
            }
          }
        }

        results =
          await connection`insert into product_temp (id, last_modified, data) values (${id}, ${lastModified}, ${
            data as unknown as SerializableParameter
          }) ON CONFLICT DO NOTHING`;

        latestModified = Math.max(latestModified, lastModified?.getTime() ?? 0);

        if (!(i % this.importBatchSize)) {
          await this.applyProductChange(connection, obsolete, source, updateId);
          await connection`begin`;
        }
        if (!(i % this.importLogInterval)) {
          this.logger.debug(`Updated ${i}`);
        }
      }
      await this.applyProductChange(connection, obsolete, source, updateId);
      await cursor.close();
      collection.count = i;
    }
    await client.close();

    // If doing a full import delete all products that weren't updated and flag all tags as imported
    if (source === ProductSource.FULL_LOAD) {
      await this.tagService.addLoadedTags(
        Object.keys(ProductTagMap.MAPPED_TAGS),
      );
      await this.deleteOtherProducts(connection, updateId);
    }

    await connection`DROP TABLE product_temp`;
    connection.release();

    this.logger.log(
      `Imported ${collections.normal.count} Products and ${collections.obsolete.count} Obsolete Products from ${source}`,
    );

    return latestModified;
  }

  async applyProductChange(
    connection: ReservedSql,
    obsolete: boolean,
    source: string,
    updateId: string,
  ) {
    // Analyze table for best query performance
    await connection`ANALYZE product_temp`;

    // Apply updates to products
    const productResults = await connection`
      UPDATE product
      SET name = tp.data->>'product_name',
        creator = tp.data->>'creator',
        owners_tags = tp.data->>'owners_tags',
        obsolete = ${obsolete},
        ingredients_count = (tp.data->>'ingredients_n')::numeric,
        ingredients_without_ciqual_codes_count = (tp.data->>'ingredients_without_ciqual_codes_n')::numeric,
        last_modified = tp.last_modified,
        last_update_id = ${updateId},
        last_updated = ${new Date()},
        source = ${source}
      FROM product_temp tp
      WHERE product.id = tp.id`;
    this.logger.debug(`Updated ${productResults.count} products`);

    // Fix ingredients
    let logText = `Updated ingredients`;
    const deleted = await connection`delete from product_ingredient 
    where product_id in (select id from product_temp)`;
    logText += ` deleted ${deleted.count},`;
    const results = await connection`insert into product_ingredient (
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
        ${obsolete}
      from product_temp product
      cross join jsonb_array_elements(data->'ingredients') with ordinality tag`;
    let affectedRows = results.count;
    logText += ` inserted ${affectedRows}`;
    while (affectedRows > 0) {
      const results = await connection`insert into product_ingredient (
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
          ${obsolete}
        from product_ingredient pi 
        join product_temp product on product.id = pi.product_id
        cross join json_array_elements(pi.data) with ordinality tag
        WHERE pi.data IS NOT NULL
        AND NOT EXISTS (SELECT * FROM product_ingredient pi2 WHERE pi2.parent_product_id = pi.product_id AND pi2.parent_sequence = pi.sequence)`;
      affectedRows = results.count;
      logText += ` > ${affectedRows}`;
    }
    this.logger.debug(logText + ' rows');

    for (const [tag, entity] of Object.entries(ProductTagMap.MAPPED_TAGS)) {
      let logText = `Updated ${tag}`;
      // Get the underlying table name for the entity
      const tableName = this.em.getMetadata(entity).tableName;

      // Delete existing tags for products that were imported on this run
      const deleted = await connection`delete from ${sql(tableName)} 
      where product_id in (select id from product_temp)`;
      logText += ` deleted ${deleted.count},`;

      // Add tags back in with the updated information
      const results = await connection`insert into ${sql(
        tableName,
      )} (product_id, value, obsolete)
        select DISTINCT id, tag.value, ${obsolete} from product_temp 
        cross join jsonb_array_elements_text(data->'${sql.unsafe(tag)}') tag`;

      logText += ` inserted ${results.count} rows`;

      this.logger.debug(logText);
    }
    await connection`truncate table product_temp`;
    await connection`commit`;
  }

  async deleteOtherProducts(connection: ReservedSql, updateId: string) {
    const deleted =
      await connection`delete from product where last_update_id != ${updateId} OR last_update_id IS NULL`;
    this.logger.debug(`${deleted.count} Products deleted`);
  }

  async scheduledImportFromMongo() {
    // Pause redis while doing a scheduled import
    await this.stopRedisConsumer();

    try {
      if (
        equal(
          Object.keys(ProductTagMap.MAPPED_TAGS).sort(),
          (await this.tagService.getLoadedTags()).sort(),
        )
      ) {
        // Do an incremental load if all tags are already loaded
        await this.importFromMongo('');
      } else {
        await this.importFromMongo();
      }
    } finally {
      // Resume redis after import
      await this.startRedisConsumer();
    }
  }

  async startRedisConsumer() {
    const redisUrl = this.settings.getRedisUrl();
    if (!redisUrl) return;
    this.client = createClient({ url: redisUrl });
    this.client.on('error', (err) => this.logger.error(err));
    await this.client.connect();
    this.receiveMessages();
  }

  async stopRedisConsumer() {
    if (this.client && this.client.isOpen) await this.client.quit();
  }

  async receiveMessages() {
    const lastMessageId = await this.settings.getLastMessageId();
    if (!this.client.isOpen) return;
    this.client
      .xRead(
        commandOptions({
          isolated: true,
        }),
        [
          // XREAD can read from multiple streams, starting at a
          // different ID for each...
          {
            key: 'product_updates_off',
            id: lastMessageId,
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
            /** Message looks like this:
              {
                code: "0850026029062",
                flavor: "off",
                user_id: "stephane",
                action: "updated",
                comment: "Modification : Remove changes",
                diffs: "{\"fields\":{\"change\":[\"categories\"],\"delete\":[\"product_name\",\"product_name_es\"]}}",
              }
             */
            await this.messages.create(messages);
            const productCodes = messages.map((m) => m.message.code);
            const filter = { code: { $in: productCodes } };
            await this.importWithFilter(filter, ProductSource.EVENT);
            await this.settings.setLastMessageId(
              messages[messages.length - 1].id,
            );
          }
        }
        setTimeout(() => {
          this.receiveMessages();
        }, 0);
      });
  }
}
