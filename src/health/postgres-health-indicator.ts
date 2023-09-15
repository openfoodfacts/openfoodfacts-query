import { EntityManager } from '@mikro-orm/core';
import { Injectable } from '@nestjs/common';
import {
  HealthIndicator,
  HealthIndicatorResult,
  HealthCheckError,
} from '@nestjs/terminus';
import { Product } from '../domain/entities/product';

@Injectable()
export class PostgresHealthIndicator extends HealthIndicator {
  NAME = 'postgres';
  constructor(private em: EntityManager) {
    super();
  }
  async isHealthy(): Promise<HealthIndicatorResult> {
    try {
      await this.em.find(Product, { code: 'x' });
      return this.getStatus(this.NAME, true);
    } catch (e) {
      throw new HealthCheckError(
        'Postgres check failed',
        this.getStatus(this.NAME, false, e),
      );
    }
  }
}
