import {
  Entity,
  Index,
  ManyToOne,
  PrimaryKey,
  Property,
} from '@mikro-orm/core';
import { Product } from './product';
import { Country } from './country';

@Entity()
@Index({
  name: 'product_scans_by_country_ix1',
  expression:
    'create index product_scans_by_country_ix1 on product_scans_by_country (year, country_id, unique_scans DESC, product_id)',
})
export class ProductScansByCountry {
  @ManyToOne({ primary: true, onDelete: 'cascade' })
  product: Product;

  @PrimaryKey({ columnType: 'smallint' })
  year: number;

  @ManyToOne({ primary: true, onDelete: 'cascade' })
  country: Country;

  @Property()
  uniqueScans: number;
}
