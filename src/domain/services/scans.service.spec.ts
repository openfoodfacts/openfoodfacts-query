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
          // This one shouldn't be included in the totals
          [ScansService.oldestYear - 1]: {
            scans_n: 3,
            unique_scans_n: 2,
            unique_scans_n_by_country: {
              uk: 2,
              world: 2,
            },
          },
          [ScansService.oldestYear]: {
            scans_n: 7,
            unique_scans_n: 3,
            unique_scans_n_by_country: {
              uk: 3,
              world: 3,
            },
          },
          [ScansService.currentYear]: {
            scans_n: 10,
            unique_scans_n: 7,
            unique_scans_n_by_country: {
              uk: 2,
              fr: 5,
              world: 7,
            },
          },
        },
        [ScansService.currentYear]: {
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
      expect(result).toHaveLength(7);

      const productCountries = await sql`SELECT * FROM product_country pc
        JOIN country c ON c.id = pc.country_id 
        WHERE product_id = (SELECT id from product where code = ${code1})
        AND c.code = 'uk'`;
      expect(productCountries).toHaveLength(1);
      expect(productCountries[0].recent_scans).toBe(2);
      expect(productCountries[0].total_scans).toBe(5);
      expect(productCountries[0].obsolete).toBe(false);
    });
  });
});
