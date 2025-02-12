import { Entity, ManyToOne, PrimaryKey, Property } from '@mikro-orm/core';
import { Product } from './product';

@Entity()
export class ProductScans {
  @ManyToOne({ primary: true, onDelete: 'cascade' })
  product: Product;

  @PrimaryKey({ columnType: 'smallint' })
  year: number;

  @Property()
  scans: number;

  @Property()
  uniqueScans: number;
}
