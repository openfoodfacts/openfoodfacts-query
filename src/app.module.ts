import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { DomainModule } from './domain/domain.module';
import { HealthModule } from './health/health.module';
import { Cron, ScheduleModule } from '@nestjs/schedule';
import { EntityManager, RequestContext } from '@mikro-orm/core';
import { ImportService } from './domain/services/import.service';

@Module({
  imports: [DomainModule, HealthModule, ScheduleModule.forRoot()],
  controllers: [AppController],
  providers: [],
})
export class AppModule {
  constructor(
    private readonly em: EntityManager,
    private readonly importService: ImportService,
  ) {}

  // Refresh the PostgreSQL database from MongoDB at 2am every night
  @Cron('00 02 * * *')
  async refreshProducts() {
    // The request context creates a separate entity manager instance
    // which avoids clashes with other requests
    await RequestContext.createAsync(this.em, async () => {
      await this.importService.importFromMongo('');
    });
  }
}
