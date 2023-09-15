import { Controller, Get } from '@nestjs/common';
import { HealthCheckService, HealthCheck } from '@nestjs/terminus';
import { PostgresHealthIndicator } from './postgres-health-indicator';
import { MongodbHealthIndicator } from './mongodb-health-indicator';

@Controller('health')
export class HealthController {
  constructor(
    private health: HealthCheckService,
    private postgres: PostgresHealthIndicator,
    private mongodb: MongodbHealthIndicator,
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      () => this.postgres.isHealthy(),
      () => this.mongodb.isHealthy(),
    ]);
  }
}
