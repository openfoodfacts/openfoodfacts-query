import { EntityManager } from '@mikro-orm/postgresql';
import { Body, Controller, Get, Logger, Post, Query } from '@nestjs/common';
import { Product } from './domain/entities/product';
import { TAG_MAPPINGS } from './domain/entities/product-tags';
import { EntityName } from '@mikro-orm/core';
import { ImportService } from './domain/services/import.service';

@Controller()
export class AppController {
  private logger = new Logger(AppController.name);
  constructor(
    private readonly em: EntityManager,
    private readonly importService: ImportService,
  ) {}

  @Get('importfromfile?')
  async importFromFile(@Query('from') from = null) {
    await this.importService.importFromFile(from);
  }

  @Get('importfrommongo?')
  async importFromMongo(@Query('from') from = null) {
    await this.importService.importFromMongo(from);
  }

  @Post('aggregate')
  async aggregate(@Body() body: any[]) {
    const start = Date.now();
    this.logger.log(body);

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
    if (count) {
      qb = this.em.createQueryBuilder(qb, 'temp');
      qb.select('count(*) count');
    } else {
      qb.groupBy(column).orderBy({ ['2']: 'DESC' });
      if (limit) qb.limit(limit);
      if (skip) qb.offset(skip);
    }

    this.logger.log(qb.getFormattedQuery());
    const results = await qb.execute();
    //this.logger.log(results);
    this.logger.log(
      `Processed ${tag}${
        matchTag ? ` where ${matchTag} ${not ? '!=' : '=='} ${matchValue}` : ''
      } in ${Date.now() - start} ms. Returning ${results.length} records`,
    );
    if (count) {
      const response = {};
      response[tag] = results[0].count;
      this.logger.log(response);
      return response;
    }
    return results;
  }

  @Post('count')
  async count(@Body() body: any) {
    const start = Date.now();
    this.logger.log(body);

    const tags = Object.keys(body);
    const tag = tags[0];
    const { entity, column } = this.getEntityAndColumn(tag);
    const qb = this.em.createQueryBuilder(entity, 'pt');
    qb.select(`count(*) count`);
    qb.where('not pt.obsolete');

    let matchValue = body[tag];
    const not = matchValue?.['$ne'];
    if (not) {
      matchValue = not;
    }
    qb.andWhere(`${not ? 'NOT ' : ''}pt.${column} = ?`, [matchValue]);
    const matchTag = tags[1];
    let extraMatchLog = '';
    if (matchTag) {
      let matchValue = body[matchTag];
      const not = matchValue?.['$ne'];
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
      extraMatchLog += ` and ${matchTag} ${not ? '!=' : '=='} ${matchValue}`;
    }
    this.logger.log(qb.getFormattedQuery());
    const results = await qb.execute();
    //this.logger.log(results);
    this.logger.log(
      `Processed ${tag} ${not ? '!=' : '=='} ${matchValue}${extraMatchLog} in ${
        Date.now() - start
      } ms.`,
    );
    const response = results[0].count;
    this.logger.log(response);
    return response;
  }

  private getEntityAndColumn(tag: any) {
    let entity: EntityName<object>;
    let column = 'value';
    if (this.importService.fields.includes(tag)) {
      entity = Product;
      column = tag;
    } else {
      entity = TAG_MAPPINGS[tag];
    }
    return { entity, column };
  }
}
