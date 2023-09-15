import { HealthController } from './health.controller';
import { createTestingModule } from '../../test/test.helper';
import { AppModule } from '../app.module';
import { MongodbHealthIndicator } from './mongodb-health-indicator';
import { HealthCheckError, HealthIndicatorResult } from '@nestjs/terminus';
import { ServiceUnavailableException } from '@nestjs/common';

describe('HealthController', () => {
  it('should return healthy', async () => {
    await createTestingModule([AppModule], async (app) => {
      const controller = app.get(HealthController);
      expect(controller).toBeDefined();

      const mongoIndicator = app.get(MongodbHealthIndicator);
      mongoIndicator.isHealthy = jest.fn(async () => {
        return {
          mongodb: {
            status: 'up',
          },
        } as HealthIndicatorResult;
      });
      const status = await controller.check();
      expect(status.status).toBe('ok');
    });
  });

  it('should return unhealthy if mongodb is down', async () => {
    await createTestingModule([AppModule], async (app) => {
      const controller = app.get(HealthController);

      const mongoIndicator = app.get(MongodbHealthIndicator);
      mongoIndicator.isHealthy = jest.fn(async () => {
        throw new HealthCheckError('Mongodb check failed', {
          mongodb: {
            status: 'down',
          },
        });
      });
      try {
        await controller.check();
        fail('should not get here');
      } catch (e) {
        expect(e).toBeInstanceOf(ServiceUnavailableException);
        expect(e.response.status).toBe('error');
      }
    });
  });
});
