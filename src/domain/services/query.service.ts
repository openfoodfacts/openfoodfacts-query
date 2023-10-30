import { EntityName } from '@mikro-orm/core';
import { EntityManager, QueryBuilder } from '@mikro-orm/postgresql';
import {
  Injectable,
  Logger,
  UnprocessableEntityException,
} from '@nestjs/common';
import { MAPPED_TAGS } from '../entities/product-tags';
import { MAPPED_FIELDS, Product } from '../entities/product';
import { TagService } from './tag.service';

@Injectable()
export class QueryService {
  private logger = new Logger(QueryService.name);
  constructor(
    private readonly em: EntityManager,
    private readonly tagService: TagService,
  ) {}

  async aggregate(body: any[]) {
    const start = Date.now();
    this.logger.debug(body);

    const match = body.find((o: any) => o['$match'])?.['$match'];
    const group = body.find((o: any) => o['$group'])?.['$group'];
    const count = body.some((o: any) => o['$count']);
    const limit = body.find((o: any) => o['$limit'])?.['$limit'];
    const skip = body.find((o: any) => o['$skip'])?.['$skip'];

    let tag = group['_id'].substring(1);
    if (tag === 'users_tags') tag = 'creator';

    const { entity, column } = await this.getEntityAndColumn(tag);
    let qb = this.em.createQueryBuilder(entity, 'pt');
    if (!count) {
      qb.select(`${column} _id, count(*) count`);
    } else {
      qb.select(`${column}`).distinct();
    }
    qb.where(this.obsoleteWhere(match));

    const whereLog = await this.addMatches(match, qb, entity);

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
    //this.logger.log(results);
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

  private async addMatches(match: any, qb: QueryBuilder<object>, parentEntity) {
    const whereLog = [];
    for (const [matchTag, matchValue] of Object.entries(match)) {
      let whereValue = matchValue;
      const not = matchValue?.['$ne'];
      if (not) {
        whereValue = not;
      }
      const { entity: matchEntity, column: matchColumn } =
        await this.getEntityAndColumn(matchTag);

      const all = whereValue?.['$all'];
      const matchValues = all ?? [whereValue];
      for (const value of matchValues) {
        const qbWhere = this.em
          .createQueryBuilder(matchEntity, 'pt2')
          .select('*')
          .where(
            `pt2.${this.productId(matchEntity)} = pt.${this.productId(
              parentEntity,
            )} and pt2.${matchColumn} = ?`,
            [value],
          );
        qb.andWhere(`${not ? 'NOT ' : ''}EXISTS (${qbWhere.getKnexQuery()})`);
        whereLog.push(`${matchTag} ${not ? '!=' : '=='} ${value}`);
      }
    }
    return whereLog;
  }

  productId(entity) {
    return entity === Product ? 'id' : 'product_id';
  }

  obsoleteWhere(body: any) {
    const obsolete = !!body?.obsolete;
    delete body?.obsolete;
    return `${obsolete ? '' : 'not '}pt.obsolete`;
  }

  async count(body: any) {
    const start = Date.now();
    this.logger.debug(body);

    const obsoleteWhere = this.obsoleteWhere(body);
    const tags = Object.keys(body ?? {});
    const tag = tags?.[0];
    const { entity, column } = await this.getEntityAndColumn(tag);
    const qb = this.em.createQueryBuilder(entity, 'pt');
    qb.select(`count(*) count`);
    qb.where(obsoleteWhere);

    const whereLog = [];
    if (tag) {
      let matchValue = body[tag];
      const not = matchValue?.['$ne'];
      if (not) {
        matchValue = not;
      }
      let all = matchValue?.['$all'];
      if (all) {
        matchValue = all.shift();
        // If only one all then will want to delete it
        if (!all.length) all = false;
      }
      whereLog.push(`${tag} ${not ? '!=' : '=='} ${matchValue}`);
      qb.andWhere(`${not ? 'NOT ' : ''}pt.${column} = ?`, [matchValue]);
      if (!all) {
        delete body[tag];
      }
      whereLog.push(...(await this.addMatches(body, qb, entity)));
    }

    this.logger.debug(qb.getFormattedQuery());
    const results = await qb.execute();
    const response = results[0].count;
    this.logger.log(
      `Processed ${whereLog.join(' and ')} in ${
        Date.now() - start
      } ms. Count: ${response}`,
    );
    return parseInt(response);
  }

  async select(body: any) {
    const start = Date.now();
    this.logger.debug(body);

    const obsoleteWhere = this.obsoleteWhere(body);
    const entity: EntityName<object> = Product;
    const qb = this.em.createQueryBuilder(entity, 'pt');
    qb.select(`*`);
    qb.where(obsoleteWhere);

    const whereLog = await this.addMatches(body, qb, entity);

    this.logger.debug(qb.getFormattedQuery());
    const results = await qb.execute();
    this.logger.log(
      `Processed ${whereLog.join(' and ')} in ${
        Date.now() - start
      } ms. Selected ${results.length} records`,
    );
    return results;
  }

  private async getEntityAndColumn(tag: any) {
    let entity: EntityName<object>;
    let column = 'value';
    if (!tag || MAPPED_FIELDS.includes(tag)) {
      entity = Product;
      column = tag;
    } else {
      entity = MAPPED_TAGS[tag];
      if (entity) {
        if (!(await this.tagService.getLoadedTags()).includes(tag)) {
          const message = `Tag '${tag}' is not loaded`;
          this.logger.warn(message);
          throw new UnprocessableEntityException(message);
        }
      }
    }
    if (entity == null) {
      const message = `Tag '${tag}' is not supported`;
      this.logger.warn(message);
      throw new UnprocessableEntityException(message);
    }
    return { entity, column };
  }
}
