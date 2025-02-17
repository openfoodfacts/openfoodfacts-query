import { Injectable, Logger } from '@nestjs/common';
import sql from '../../db';

export type ProductScanList = {
  [code: string]: {
    [year: string]: {
      scans_n: number;
      unique_scans_n: number;
      unique_scans_n_by_country: {
        [countryCode: string]: number;
      };
    };
  };
};

@Injectable()
export class ScansService {
  private logger = new Logger(ScansService.name);
  public static currentYear = 2024;
  public static oldestYear = 2019;

  async create(scans: ProductScanList) {
    const scansByCountry = Object.entries(scans)
      .map(([code, years]) =>
        Object.entries(years)
          .map(([year, scanCounts]) =>
            Object.entries(scanCounts.unique_scans_n_by_country).map(
              ([country, count]) => [code, year, country, count],
            ),
          )
          .flat(),
      )
      .flat();

    const inserted =
      await sql`INSERT INTO product_scans_by_country (product_id, year, country_id, unique_scans) 
        SELECT product.id, source.year::int, country.id, source.scans::int 
        FROM (values ${sql(
          scansByCountry,
        )}) as source (code, year, country, scans)
        JOIN product ON product.code = source.code
        JOIN country ON country.code = source.country
        ON CONFLICT (product_id, year, country_id) 
        DO UPDATE SET unique_scans = EXCLUDED.unique_scans
        RETURNING product_id`;

    const idsUpdated = [...new Set(inserted.map((i) => i.product_id))];
    // TODO: Remove country entries that are not referenced by a counties_tag

    await sql`INSERT INTO product_country (product_id, country_id, recent_scans, total_scans)
      SELECT product_id, country_id, unique_scans, unique_scans
      FROM product_scans_by_country
      WHERE product_id in ${sql(idsUpdated)}
      AND year = ${ScansService.currentYear}
      ON CONFLICT (product_id, country_id)
      DO UPDATE SET recent_scans = EXCLUDED.recent_scans`;

    await sql`INSERT INTO product_country (product_id, country_id, recent_scans, total_scans)
      SELECT product_id, country_id, 0, sum(unique_scans)
      FROM product_scans_by_country
      WHERE product_id in ${sql(idsUpdated)}
      AND year >= ${ScansService.oldestYear}
      GROUP BY product_id, country_id
      ON CONFLICT (product_id, country_id)
      DO UPDATE SET total_scans = EXCLUDED.total_scans`;

    this.logger.log(`Received scans for ${Object.keys(scans).length} products`);
  }
}
