import { Body, Controller, Get, Post, Query, All } from '@nestjs/common';
import { ImportService } from './domain/services/import.service';
import { QueryService } from './domain/services/query.service';
import { RedisListener } from './domain/services/redis.listener';

@Controller()
export class AppController {
  constructor(
    private readonly importService: ImportService,
    private readonly queryService: QueryService,
    private readonly redisListener: RedisListener,
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
  async select(@Body() body: any, @Query('obsolete') obsolete) {
    return await this.queryService.select(body, this.parseBoolean(obsolete));
  }
}
