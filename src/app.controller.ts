import { Body, Controller, Get, Post, Query, All } from '@nestjs/common';
import { ImportService } from './domain/services/import.service';
import { QueryService } from './domain/services/query.service';

@Controller()
export class AppController {
  constructor(
    private readonly importService: ImportService,
    private readonly queryService: QueryService,
  ) {}

  @Get('importfromfile')
  async importFromFile(@Query('from') from = null) {
    await this.importService.importFromFile(from);
  }

  @Get('importfrommongo')
  async importFromMongo(
    @Query('from') from = null,
    @Query('skip') skip = null,
  ) {
    await this.importService.importFromMongo(from, skip);
  }

  @Get('scheduledimportfrommongo')
  async scheduledImportFromMongo() {
    await this.importService.scheduledImportFromMongo();
  }

  @Get('updatetags')
  async updateTags(@Query('updateid') updateId) {
    await this.importService.updateTags(updateId, true);
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
