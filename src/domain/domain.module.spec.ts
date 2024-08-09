import { createTestingModule } from '../../test/test.helper';
import { DomainModule } from './domain.module';
import { ImportService } from './services/import.service';
import { RedisListener } from './services/redis.listener';

describe('refreshProducts', () => {
  it('should pause Redis while doing a scheduled reload', async () => {
    await createTestingModule([DomainModule], async (app) => {
      const importService = app.get(ImportService);
      const redisListener = app.get(RedisListener);
      jest.spyOn(importService, 'importFromMongo').mockImplementation();
      const redisStopSpy = jest
        .spyOn(redisListener, 'stopRedisConsumer')
        .mockImplementation();
      const redisStartSpy = jest
        .spyOn(redisListener, 'startRedisConsumer')
        .mockImplementation();

      await app.get(DomainModule).refreshProducts();
      expect(redisStopSpy).toHaveBeenCalledTimes(1);
      expect(redisStartSpy).toHaveBeenCalledTimes(1);
    });
  });
});
