import { Body, Controller, Get, Post, Query, All } from '@nestjs/common';
import { ImportService } from './domain/services/import.service';
import { QueryService } from './domain/services/query.service';
import { RedisListener } from './domain/services/redis.listener';
import { MessagesService } from './domain/services/messages.service';
import { ProductScanList, ScansService } from './domain/services/scans.service';
import {
  AggregateQuery,
  Filter,
  FindQuery,
} from './domain/dto/query-interface';

@Controller()
export class AppController {
  constructor(
    private readonly importService: ImportService,
    private readonly queryService: QueryService,
    private readonly redisListener: RedisListener,
    private readonly messagesService: MessagesService,
    private readonly scansService: ScansService,
  ) {}

  @Get('importfrommongo')
  async importFromMongo(
    @Query('from') from = null,
    @Query('skip') skip = null,
  ) {
    await this.importService.importFromMongo(from, skip);
  }

  @Get('scheduledimportfrommongo')
  async scheduledImportFromMongo() {
    // Pause redis while doing a scheduled import
    await this.redisListener.pauseAndRun(
      async () => await this.importService.scheduledImportFromMongo(),
    );
  }

  parseBoolean(value) {
    return value == true || value?.toLowerCase() == 'true';
  }

  @Post('aggregate')
  async aggregate(@Body() body: AggregateQuery, @Query('obsolete') obsolete) {
    return await this.queryService.aggregate(body, this.parseBoolean(obsolete));
  }

  @All('count')
  async count(@Body() body: Filter, @Query('obsolete') obsolete) {
    return await this.queryService.count(body, this.parseBoolean(obsolete));
  }

  @Post('select')
  async select(@Body() body: Filter) {
    return await this.queryService.select(body);
  }

  @Post('find')
  async find(@Body() body: FindQuery, @Query('obsolete') obsolete) {
    return await this.queryService.find(body, obsolete);
  }

  // Temporary code for initial import
  messageId = 0;
  @Post('productupdates')
  async addProductUpdates(@Body() updates: any[]) {
    const messages = [];
    for (const update of updates) {
      messages.push({ id: `0-${this.messageId++}`, message: update });
    }
    await this.messagesService.create(messages, true);
  }

  @Post('scans')
  async addProductScans(
    @Body() scans: ProductScanList,
    @Query('fullyloaded') fullyLoaded = false,
  ) {
    await this.scansService.create(scans, fullyLoaded);
  }
}
