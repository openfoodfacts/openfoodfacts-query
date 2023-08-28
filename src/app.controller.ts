import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ImportService } from './domain/services/import.service';
import { QueryService } from './domain/services/query.service';

@Controller()
export class AppController {
  constructor(
    private readonly importService: ImportService,
    private readonly queryService: QueryService,
  ) {}

  @Get('importfromfile?')
  async importFromFile(@Query('from') from = null) {
    await this.importService.importFromFile(from);
  }

  @Get('importfrommongo?')
  async importFromMongo(
    @Query('from') from = null,
    @Query('skip') skip = null,
  ) {
    await this.importService.importFromMongo(from, skip);
  }

  @Post('aggregate')
  async aggregate(@Body() body: any[]) {
    return await this.queryService.aggregate(body);
  }

  @Post('count')
  async count(@Body() body: any) {
    return await this.queryService.count(body);
  }
}
