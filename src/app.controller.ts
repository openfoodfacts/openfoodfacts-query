import { Body, Controller, Get, Post, Query, All } from '@nestjs/common';
import { ImportService } from './domain/services/import.service';
import { QueryService } from './domain/services/query.service';
import { RedisListener } from './domain/services/redis.listener';
import { MessagesService } from './domain/services/messages.service';
import { ProductScanList, ScansService } from './domain/services/scans.service';

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
      this.importService.scheduledImportFromMongo,
    );
  }

  parseBoolean(value) {
    return value == true || value?.toLowerCase() == 'true';
  }

  @Post('aggregate')
  async aggregate(@Body() body: any[], @Query('obsolete') obsolete) {
    return await this.queryService.aggregate(body, this.parseBoolean(obsolete));
  }

  @All('count')
  async count(@Body() body: any, @Query('obsolete') obsolete) {
    return await this.queryService.count(body, this.parseBoolean(obsolete));
  }

  @Post('select')
  async select(@Body() body: any) {
    return await this.queryService.select(body);
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
  async addProductScans(@Body() scans: ProductScanList) {
    await this.scansService.create(scans);
  }
}
