import { createTestingModule, randomCode } from '../../../test/test.helper';
import sql from '../../db';
import { DomainModule } from '../domain.module';
import { addAllCountries } from '../entities/country';
import { ScansService } from './scans.service';

describe('create', () => {
  it('should create product scans', async () => {
    await createTestingModule([DomainModule], async (app) => {
      // Refresh country table
      await addAllCountries();

      const scansService = app.get(ScansService);

      // Create some products
      const code1 = randomCode();
      const code2 = randomCode();
      await sql`INSERT INTO product ${sql([
        {
          code: code1,
        },
        {
          code: code2,
        },
      ])}`;

      await scansService.create({
        [code1]: {
          '2023': {
            scans_n: 7,
            unique_scans_n: 3,
            unique_scans_n_by_country: {
              uk: 3,
              world: 3,
            },
          },
          '2024': {
            scans_n: 10,
            unique_scans_n: 7,
            unique_scans_n_by_country: {
              uk: 2,
              fr: 5,
              world: 7,
            },
          },
        },
        [code2]: {
          '2024': {
            scans_n: 11,
            unique_scans_n: 8,
            unique_scans_n_by_country: {
              ru: 1,
              fr: 4,
              world: 5,
            },
          },
        },
      });
      const result =
        await sql`SELECT * FROM product_scans_by_country WHERE product_id = (SELECT id from product where code = ${code1})`;
      expect(result).toHaveLength(5);
    });
  });
});
