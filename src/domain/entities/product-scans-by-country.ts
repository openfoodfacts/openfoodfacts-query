import { Entity, ManyToOne, PrimaryKey, Property } from '@mikro-orm/core';
import { Product } from './product';
import { Country } from './country';

@Entity()
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
