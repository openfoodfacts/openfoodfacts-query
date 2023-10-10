import { EntityName } from '@mikro-orm/core';
import { EntityManager, QueryBuilder } from '@mikro-orm/postgresql';
import {
  Injectable,
  Logger,
  UnprocessableEntityException,
} from '@nestjs/common';
import { MAPPED_TAGS } from '../entities/product-tags';
import { MAPPED_FIELDS, Product } from '../entities/product';

@Injectable()
export class QueryService {
  private logger = new Logger(QueryService.name);
  constructor(private readonly em: EntityManager) {}

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

    const { entity, column } = this.getEntityAndColumn(tag);
    let qb = this.em.createQueryBuilder(entity, 'pt');
    if (!count) {
      qb.select(`${column} _id, count(*) count`);
    } else {
      qb.select(`${column}`).distinct();
    }
    qb.where('not pt.obsolete');

    const whereLog = this.addMatches(match, qb);

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

  private addMatches(match: any, qb: QueryBuilder<object>, parentKey = 'pt.product_id') {
    const whereLog = [];
    for (const [matchTag, matchValue] of Object.entries(match)) {
      let whereValue = matchValue;
      const not = matchValue?.['$ne'];
      if (not) {
        whereValue = not;
      }
      const { entity: matchEntity, column: matchColumn } =
        this.getEntityAndColumn(matchTag);
      const qbWhere = this.em
        .createQueryBuilder(matchEntity, 'pt2')
        .select('*')
        .where(`pt2.product_id = ${parentKey} and pt2.${matchColumn} = ?`, [
          whereValue,
        ]);
      qb.andWhere(`${not ? 'NOT ' : ''}EXISTS (${qbWhere.getKnexQuery()})`);
      whereLog.push(`${matchTag} ${not ? '!=' : '=='} ${whereValue}`);
    }
    return whereLog;
  }

  async count(body: any) {
    const start = Date.now();
    this.logger.debug(body);
    const obsolete = !!body?.obsolete;
    if (obsolete) delete body.obsolete;

    const tags = Object.keys(body ?? {});
    const tag = tags?.[0];
    const { entity, column } = this.getEntityAndColumn(tag);
    const qb = this.em.createQueryBuilder(entity, 'pt');
    qb.select(`count(*) count`);
    qb.where(`${obsolete ? '' : 'not '}pt.obsolete`);

    let whereLog = [];
    if (tag) {
      let matchValue = body[tag];
      const not = matchValue?.['$ne'];
      whereLog.push(`${tag} ${not ? '!=' : '=='} ${matchValue}`);
      if (not) {
        matchValue = not;
      }
      qb.andWhere(`${not ? 'NOT ' : ''}pt.${column} = ?`, [matchValue]);
      delete body[tag];
      whereLog.push(...this.addMatches(body, qb));
    }

    this.logger.debug(qb.getFormattedQuery());
    const results = await qb.execute();
    const response = results[0].count;
    this.logger.log(
      `Processed ${whereLog.join(' and ')} in ${Date.now() - start} ms. Count: ${response}`,
    );
    return parseInt(response);
  }

  async select(body: any) {
    const start = Date.now();
    this.logger.debug(body);

    const tags = Object.keys(body);
    let entity: EntityName<object> = Product;
    const qb = this.em.createQueryBuilder(entity, 'p');
    qb.select(`*`);
    qb.where('not p.obsolete');

    const whereLog = this.addMatches(body, qb, 'p.id');

    this.logger.debug(qb.getFormattedQuery());
    const results = await qb.execute();
    return results;
  }

  private getEntityAndColumn(tag: any) {
    let entity: EntityName<object>;
    let column = 'value';
    if (!tag || MAPPED_FIELDS.includes(tag)) {
      entity = Product;
      column = tag;
    } else {
      entity = MAPPED_TAGS[tag];
    }
    if (entity == null) {
      const message = `Tag '${tag}' is not supported`;
      this.logger.warn(message);
      throw new UnprocessableEntityException(message);
    }
    return { entity, column };
  }
}
