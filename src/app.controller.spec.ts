import { createTestingModule, randomCode } from '../test/test.helper';
import { AppController } from './app.controller';
import { AppModule } from './app.module';
import sql from './db';
import { ImportService } from './domain/services/import.service';

describe('productupdate', () => {
  it('should import message but not refresh products', async () => {
    await createTestingModule([AppModule], async (app) => {
      const importService = app.get(ImportService);
      const importSpy = jest
        .spyOn(importService, 'importWithFilter')
        .mockImplementation();

      const code1 = randomCode();
      const updates = [
        {
          code: code1,
          rev: 1,
        },
      ];

      const appController = app.get(AppController);
      await appController.addProductUpdates(updates);

      // Then the import is not called
      expect(importSpy).not.toHaveBeenCalled();

      // Update events are created
      const events =
        await sql`SELECT * FROM product_update_event WHERE message->>'code' = ${code1}`;

      expect(events).toHaveLength(1);
    });
  });
});
