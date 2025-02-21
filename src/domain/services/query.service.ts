import { EntityName } from '@mikro-orm/core';
import { EntityManager, QueryBuilder } from '@mikro-orm/postgresql';
import {
  Injectable,
  Logger,
  UnprocessableEntityException,
} from '@nestjs/common';
import { MAPPED_FIELDS, Product } from '../entities/product';
import { TagService } from './tag.service';
import { ProductTagMap } from '../entities/product-tag-map';
import { MongoClient } from 'mongodb';
import sql from '../../db';
import { ProductCountry } from '../entities/product-country';

@Injectable()
export class QueryService {
  private logger = new Logger(QueryService.name);
  constructor(
    private readonly em: EntityManager,
    private readonly tagService: TagService,
  ) {}

  /** Uses the MongoDB aggregate pipeline style query to return counts grouped by a specified facet */
  async aggregate(body: any[], obsolete = false) {
    const start = Date.now();
    this.logger.debug(body);

    // Match includes any filter criteria
    const match = body.find((o: any) => o['$match'])?.['$match'];

    // Group indicates what field to group results by
    const group = body.find((o: any) => o['$group'])?.['$group'];

    // If count is specified then this just counts the number of distinct facet values
    const count = body.some((o: any) => o['$count']);

    // Limit and skip support paging of large results (like ingredients)
    const limit = body.find((o: any) => o['$limit'])?.['$limit'];
    const skip = body.find((o: any) => o['$skip'])?.['$skip'];

    let tag = group['_id'].substring(1);
    if (tag === 'users_tags') tag = 'creator';

    // Determine which entity to query (Product or a specific Tag table)
    const { entity, column } = await this.getEntityAndColumn(tag);
    let qb = this.em.createQueryBuilder(entity, 'pt');
    if (!count) {
      qb.select(`${column} _id, count(*) count`);
    } else {
      qb.select(`${column}`).distinct();
    }
    // Add the where clause that determines whether to fetch obsolete products or not
    qb.where(this.obsoleteWhere(obsolete));

    // Add filter criteria to the where clause
    const whereLog = await this.addMatches(this.parseFilter(match), qb, entity);

    if (count) {
      qb = this.em.createQueryBuilder(qb, 'temp');
      qb.select('count(*) count');
    } else {
      qb.groupBy(column).orderBy({ ['2']: 'DESC' });
      if (limit) qb.limit(limit);
      if (skip) qb.offset(skip);
    }

    this.logger.debug(qb.getFormattedQuery());
    const results = await qb.execute();
    this.logger.debug(
      `Processed ${tag}${
        whereLog.length ? ` where ${whereLog.join(' and ')}` : ''
      } in ${Date.now() - start} ms. Returning ${results.length} records`,
    );
    if (count) {
      const response = {};
      response[tag] = results[0].count;
      this.logger.debug(response);
      return response;
    }
    return results;
  }

  /**
   * Turns the filter into a simple list of tags and values that can be "anded" together
   * note this doesn't currently support "or" operations
   */
  private parseFilter(matches): [string, any][] {
    const filters = [];
    for (const filter of Object.entries(matches)) {
      if (filter[0] === '$and') {
        // If the key is $and then the value will be an array of objects, e.g.
        // $and: [
        //   { amino_acids_tags: "value1" },
        //   { amino_acids_tags: "value2" },
        // ]
        // Expand these to just appear as additional filter entries
        for (const subFilter of filter[1] as []) {
          filters.push(...this.parseFilter(subFilter));
        }
      } else {
        const all = filter[1]['$all'];
        if (all) {
          // All is very similar to $and except that it is specified for the values, e.g.
          // amino_acids_tags: { $all: ["value1", "value1"] }
          // Simply append these as multiple tag / value pairs for the same tag
          for (const value of all) {
            filters.push([filter[0], value]);
          }
        } else {
          filters.push(filter);
        }
      }
    }
    return filters;
  }

  /**
   * Iterates over the list of tag / value pairs and adds them as where clauses to the supplied QueryBuilder.
   * @param filters The list of tag / value pairs
   * @param qb The QueryBuilder to add the where clause to
   * @param parentEntity Determines the column in which the product id is found in the perant
   * @returns A human-readable summary of the clauses added
   */
  private async addMatches(
    filters: [string, any][],
    qb: QueryBuilder<object>,
    parentEntity,
  ) {
    const whereLog = [];
    for (const [matchTag, matchValue] of filters) {
      const { entity: matchEntity, column: matchColumn } =
        await this.getEntityAndColumn(matchTag);

      let whereValue = matchValue;
      // If $ne is specified then a not equal query is needed, e.g.
      // additives_tags: { $ne: "value1" }
      let not = matchValue?.['$ne'];
      if (not) {
        whereValue = not;
      }
      // If the value is still an object then we can't handle it
      if (whereValue === Object(whereValue)) {
        // Unless it is an $in
        const keys = Object.keys(whereValue);
        let operator = keys[0];
        if (
          keys.length != 1 ||
          !['$in', '$nin'].includes(operator) ||
          !whereValue[operator].length
        )
          this.throwUnprocessableException(
            `Unable to process ${JSON.stringify(whereValue)}`,
          );

        // Do a NOT EXISTS WHERE IN () for $nin. Should work for Product as well as tags
        if (operator === '$nin') {
          whereValue = { $in: whereValue['$nin'] };
          operator = '$in';
          not = !not;
        }

        // $in contents must all be scalars
        for (const value of whereValue[operator]) {
          if (value == null || value.length === 0) {
            // For MongoDB $in: [null, []] is used as an "IS NULL" / "NOT EXISTS"
            // If the query is on the product table we want an is null where, otherwise we want a not exists
            if (matchEntity === Product) {
              whereValue = null;
            } else {
              not = !not;
              whereValue = undefined;
            }
            // only use case for having null or [] is this one, exit
            break;
          }
          if (value === Object(value))
            this.throwUnprocessableException(
              `Unable to process ${JSON.stringify(whereValue)}`,
            );
        }
      }

      // The following creates an EXISTS / NOT EXISTS sub-query for the specified tag
      const knex = this.em.getKnex();

      // Join to the parent table
      const where = {
        [`pt2.${this.productId(matchEntity)}`]: knex.ref(
          `pt.${this.productId(parentEntity)}`,
        ),
      };
      // Add the specific criteria. whereValue will be undefined for a full exists / not exists
      if (whereValue !== undefined) where[`pt2.${matchColumn}`] = whereValue;

      const qbWhere = this.em
        .createQueryBuilder(matchEntity, 'pt2')
        .select('*')
        .where(where);
      qb.andWhere(`${not ? 'NOT ' : ''}EXISTS (${qbWhere.getKnexQuery()})`);
      whereLog.push(`${matchTag} ${not ? '!=' : '=='} ${whereValue}`);
    }
    return whereLog;
  }

  /** Determins the name of the product id field */
  productId(entity) {
    return entity === Product ? 'id' : 'product_id';
  }

  /** Returns a where expression for the onsolete flag */
  obsoleteWhere(obsolete: boolean) {
    return `${obsolete ? '' : 'not '}pt.obsolete`;
  }

  /** Counts the number of document meeting the specified criteria */
  async count(body: any, obsolete = false) {
    const start = Date.now();
    this.logger.debug(body);

    const filters = this.parseFilter(body ?? {});

    // Always use product as the main table  otherwise "nots" are not handled correctly
    const entity: EntityName<object> = Product;
    const qb = this.em.createQueryBuilder(entity, 'pt');
    qb.select(`count(*) count`);
    qb.where(this.obsoleteWhere(obsolete));

    // Add where clauses
    const whereLog = await this.addMatches(filters, qb, entity);

    this.logger.debug(qb.getFormattedQuery());
    const results = await qb.execute();
    const response = results[0].count;
    this.logger.debug(
      `Processed ${whereLog.join(' and ')} in ${
        Date.now() - start
      } ms. Count: ${response}`,
    );
    return parseInt(response);
  }

  /** Fetches the entire document record for the filter. Not used by Product Opener */
  async select(body: any) {
    const start = Date.now();
    this.logger.debug(body);

    const entity: EntityName<object> = Product;
    const qb = this.em.createQueryBuilder(entity, 'pt');
    qb.select(`*`);

    const whereLog = await this.addMatches(this.parseFilter(body), qb, entity);

    this.logger.debug(qb.getFormattedQuery());
    const results = await qb.execute();
    this.logger.debug(
      `Processed ${whereLog.join(' and ')} in ${
        Date.now() - start
      } ms. Selected ${results.length} records`,
    );
    return results;
  }

  async find(body: any): Promise<any[]> {
    const start = Date.now();
    const mainSort = body.sort?.[0][0];
    const productCodes = [];
    // Currently only do the filtering on off-query if we are sorting by popularity
    if (mainSort === 'popularity_key') {
      const countryTag = body.filter.countries_tags ?? 'en:world';
      delete body.filter.countries_tags;
      const filters = this.parseFilter(body.filter ?? {});
      const countryId = (
        await sql`SELECT id FROM country WHERE tag = ${countryTag}`
      )[0].id;
      const limit = body.limit ? sql`LIMIT ${body.limit}` : sql``;
      const offset = body.skip ? sql`OFFSET ${body.skip}` : sql``;
      const results = await sql`SELECT p.code 
          FROM product_country pt
          JOIN product p on p.id = pt.product_id
          WHERE pt.country_id = ${countryId} 
          AND NOT p.obsolete
          ${(await this.getFilterSql(filters, ProductCountry)).whereClause}
          ORDER BY pt.recent_scans DESC, pt.total_scans DESC, pt.product_id
          ${limit} ${offset}`;
      this.logger.debug(results.statement.string);
      productCodes.push(...results.map((r) => r.code));
      body.filter = { _id: { $in: productCodes } };
      delete body.sort;
      delete body.limit;
      delete body.skip;
    }

    const sqlTime = Date.now();
    this.logger.debug(body);
    const client = new MongoClient(process.env.MONGO_URI);
    await client.connect();
    const db = client.db('off');
    const products = db.collection(`products`);
    const cursor = products.find(body.filter, {
      projection: body.projection,
      sort: body.sort,
      limit: body.limit,
      skip: body.skip,
    });
    const results = [];
    while (true) {
      const data = await cursor.next();
      if (!data) break;
      const sortIndex = productCodes.indexOf(data.code);
      if (sortIndex >= 0) results[sortIndex] = data;
      else results.push(data);
    }

    await cursor.close();
    await client.close();
    this.logger.debug(
      `Retrieved ${results.length} records. ${
        productCodes.length ? `Sql: ${sqlTime - start}  ms, ` : ``
      }MongoDB: ${Date.now() - start} ms`,
    );

    return results;
    // this.throwUnprocessableException(`Query not supported`);
  }

  /**
   * Iterates over the list of tag / value pairs and returns a WHERE clause
   * @param filters The list of tag / value pairs
   * @param parentEntity Determines the column in which the product id is found in the parent
   * @returns array of sql fragment
   */
  private async getFilterSql(filters: [string, any][], parentEntity) {
    let whereClause = sql``;
    for (const [matchTag, matchValue] of filters) {
      const { entity: matchEntity, column: matchColumn } =
        await this.getEntityAndColumn(matchTag);

      let whereValue = matchValue;
      // If $ne is specified then a not equal query is needed, e.g.
      // additives_tags: { $ne: "value1" }
      let not = matchValue?.['$ne'];
      if (not) {
        whereValue = not;
      }
      // If the value is still an object then we can't handle it
      if (whereValue === Object(whereValue)) {
        // Unless it is an $in
        const keys = Object.keys(whereValue);
        let operator = keys[0];
        if (
          keys.length != 1 ||
          !['$in', '$nin'].includes(operator) ||
          !whereValue[operator].length
        )
          this.throwUnprocessableException(
            `Unable to process ${JSON.stringify(whereValue)}`,
          );

        // Do a NOT EXISTS WHERE IN () for $nin. Should work for Product as well as tags
        if (operator === '$nin') {
          whereValue = { $in: whereValue['$nin'] };
          operator = '$in';
          not = !not;
        }

        // $in contents must all be scalars
        for (const value of whereValue[operator]) {
          if (value == null || value.length === 0) {
            // For MongoDB $in: [null, []] is used as an "IS NULL" / "NOT EXISTS"
            // If the query is on the product table we want an is null where, otherwise we want a not exists
            if (matchEntity === Product) {
              whereValue = null;
            } else {
              not = !not;
              whereValue = undefined;
            }
            // only use case for having null or [] is this one, exit
            break;
          }
          if (value === Object(value))
            this.throwUnprocessableException(
              `Unable to process ${JSON.stringify(whereValue)}`,
            );
        }
      }

      // The following creates an EXISTS / NOT EXISTS sub-query for the specified tag
      const matchTable = this.em.getMetadata(matchEntity).tableName;
      let innerWhere = sql`pt2.${sql(this.productId(matchEntity))} = pt.${sql(
        this.productId(parentEntity),
      )}`;

      // Add the specific criteria. whereValue will be undefined for a full exists / not exists
      if (whereValue !== undefined)
        innerWhere = sql`${innerWhere} AND pt2.${sql(
          matchColumn,
        )} = ${whereValue}`;

      whereClause = sql`${whereClause} AND ${not ? sql`NOT` : sql``}
        EXISTS (SELECT * FROM ${sql(matchTable)} pt2 WHERE ${innerWhere})`;
    }
    // Wrap in an object as otherwise it looks like a promise
    return { whereClause };
  }

  /** Determines the entity to use for the query. */
  private async getEntityAndColumn(tag: any) {
    let entity: EntityName<object>;
    let column = 'value';
    if (!tag || MAPPED_FIELDS.includes(tag)) {
      // The field is a single value stored on the Product itself
      entity = Product;
      // TODO: This won't work where the column name does not match the tag name
      column = tag;
    } else {
      entity = ProductTagMap.MAPPED_TAGS[tag];
      if (entity) {
        // Check to see if the tag has been loaded. This allows us to introduce
        // new tags but they will initially not be supported until a full import
        // is performed
        if (!(await this.tagService.getLoadedTags()).includes(tag))
          this.throwUnprocessableException(`Tag '${tag}' is not loaded`);
      }
    }
    if (entity == null)
      this.throwUnprocessableException(`Tag '${tag}' is not supported`);

    return { entity, column };
  }

  private throwUnprocessableException(message: string) {
    this.logger.warn(message);
    throw new UnprocessableEntityException(message);
  }
}
