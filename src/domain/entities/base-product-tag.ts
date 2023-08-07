import { Index, ManyToOne, PrimaryKey, Property } from '@mikro-orm/core';
import { Product } from './product';

@Index({ properties: ['value'] })
export abstract class BaseProductTag {
  constructor(product: Product, sequence: number, value: string) {
    this.product = product;
    this.sequence = sequence;
    this.value = value;
  }

  @ManyToOne({ primary: true })
  product: Product;

  @Property()
  value: string;

  @PrimaryKey()
  sequence: number;
}
