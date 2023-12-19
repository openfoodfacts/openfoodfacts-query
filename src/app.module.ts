import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { DomainModule } from './domain/domain.module';
import { HealthModule } from './health/health.module';

@Module({
  imports: [DomainModule, HealthModule],
  controllers: [AppController],
  providers: [],
})
export class AppModule {}
