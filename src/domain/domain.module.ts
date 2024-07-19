import { MikroOrmModule } from '@mikro-orm/nestjs';
import { Module, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { ImportService } from './services/import.service';
import { QueryService } from './services/query.service';
import { TagService } from './services/tag.service';
import { SettingsService } from './services/settings.service';
import { EntityManager, RequestContext } from '@mikro-orm/core';
import { Cron, ScheduleModule } from '@nestjs/schedule';
import { MessagesService } from './services/messages.service';

@Module({
  imports: [MikroOrmModule.forRoot(), ScheduleModule.forRoot()],
  providers: [
    ImportService,
    QueryService,
    TagService,
    SettingsService,
    MessagesService,
  ],
  exports: [ImportService, QueryService, TagService, SettingsService],
})
export class DomainModule implements OnModuleInit, OnModuleDestroy {
  constructor(
    private readonly em: EntityManager,
    private readonly importService: ImportService,
  ) {}

  async onModuleInit() {
    RequestContext.create(this.em, () => {
      this.importService.startRedisConsumer();
    });
  }

  async onModuleDestroy() {
    await this.importService.stopRedisConsumer();
  }

  // Refresh the PostgreSQL database from MongoDB at 2am every night
  //@Cron('0 * * * * *') // Every minute for testing
  @Cron('00 02 * * *')
  async refreshProducts() {
    // The request context creates a separate entity manager instance
    // which avoids clashes with other requests
    await RequestContext.createAsync(this.em, async () => {
      await this.importService.scheduledImportFromMongo();
    });
  }
}
