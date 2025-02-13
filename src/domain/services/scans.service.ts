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

  async create(scans: ProductScanList) {
    const scansByYear = Object.entries(scans)
      .map(([code, years]) =>
        Object.entries(years).map(([year, scanCounts]) => [
          code,
          year,
          scanCounts.scans_n,
          scanCounts.unique_scans_n,
        ]),
      )
      .flat();

    await sql`INSERT INTO product_scans (product_id, year, scans, unique_scans) 
      SELECT product.id, source.year::int, source.scans::int, source.unique_scans::int 
      FROM (values ${sql(
        scansByYear,
      )}) as source (code, year, scans, unique_scans)
      JOIN product ON product.code = source.code
      ON CONFLICT (product_id, year) 
        DO UPDATE SET scans = EXCLUDED.scans,
          unique_scans = EXCLUDED.unique_scans`;

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

    await sql`INSERT INTO product_scans_by_country (product_id, year, country_id, unique_scans) 
        SELECT product.id, source.year::int, country.id, source.scans::int 
        FROM (values ${sql(
          scansByCountry,
        )}) as source (code, year, country, scans)
        JOIN product ON product.code = source.code
        JOIN country ON country.code = source.country
        ON CONFLICT (product_id, year, country_id) 
        DO UPDATE SET unique_scans = EXCLUDED.unique_scans`;

    this.logger.log(`Received scans for ${Object.keys(scans).length} products`);
  }
}
