import { Entity, Index, ManyToOne, Property } from '@mikro-orm/core';
import { Product } from './product';
import { Country } from './country';

@Entity()
@Index({
  name: 'product_country_ix1',
  expression:
    'create index product_country_ix1 on product_country (obsolete, country_id, recent_scans DESC, total_scans DESC, product_id)',
})
export class ProductCountry {
  @ManyToOne({ primary: true, onDelete: 'cascade' })
  product: Product;

  @Property()
  obsolete? = false;

  @ManyToOne({ primary: true, onDelete: 'cascade' })
  country: Country;

  @Property()
  recentScans: number;

  @Property()
  totalScans: number;
}
