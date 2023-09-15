import { Module } from '@nestjs/common';
import { HealthController } from './health.controller';
import { PostgresHealthIndicator } from './postgres-health-indicator';
import { TerminusModule } from '@nestjs/terminus';
import { DomainModule } from '../domain/domain.module';
import { MongodbHealthIndicator } from './mongodb-health-indicator';

@Module({
  imports: [TerminusModule, DomainModule],
  controllers: [HealthController],
  providers: [PostgresHealthIndicator, MongodbHealthIndicator],
})
export class HealthModule {}
