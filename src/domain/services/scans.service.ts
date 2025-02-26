import { Injectable, Logger } from '@nestjs/common';
import sql from '../../db';
import { normalizeCode } from '../entities/product';
import { TagService } from './tag.service';
import { ProductCountry } from '../entities/product-country';

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

  constructor(private readonly tagService: TagService) {}

  async create(scans: ProductScanList, fullyLoaded = false) {
    const start = Date.now();

    const scansByCountry = Object.entries(scans)
      .map(([code, years]) =>
        Object.entries(years)
          .map(([year, scanCounts]) =>
            Object.entries(scanCounts.unique_scans_n_by_country).map(
              ([country, count]) => [normalizeCode(code), year, country, count],
            ),
          )
          .flat(),
      )
      .flat();

    if (scansByCountry.length) {
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

      // TODO: Need to reset recent_scans and total_scans to zero if there are none in the
      // relevant time-frame
      await sql`INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT product_id, p.obsolete, country_id, unique_scans, unique_scans
        FROM product_scans_by_country
        JOIN product p ON p.id = product_id
        WHERE product_id in ${sql(idsUpdated)}
        AND year = ${ScansService.currentYear}
        ON CONFLICT (product_id, country_id)
        DO UPDATE SET recent_scans = EXCLUDED.recent_scans, obsolete = EXCLUDED.obsolete`;

      await sql`INSERT INTO product_country (product_id, obsolete, country_id, recent_scans, total_scans)
        SELECT product_id, p.obsolete, country_id, 0, sum(unique_scans)
        FROM product_scans_by_country
        JOIN product p ON p.id = product_id
        WHERE product_id in ${sql(idsUpdated)}
        AND year >= ${ScansService.oldestYear}
        GROUP BY product_id, p.obsolete, country_id
        ON CONFLICT (product_id, country_id)
        DO UPDATE SET total_scans = EXCLUDED.total_scans, obsolete = EXCLUDED.obsolete`;
    }

    if (fullyLoaded) await this.tagService.addLoadedTags([ProductCountry.TAG]);

    this.logger.log(
      `Processed scans for ${Object.keys(scans).length} products in ${
        Date.now() - start
      } ms.${fullyLoaded ? '. All scans now loaded.' : ''}`,
    );
  }
}
