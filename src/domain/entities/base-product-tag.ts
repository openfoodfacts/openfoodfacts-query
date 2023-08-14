import { ManyToOne, PrimaryKey, Property } from '@mikro-orm/core';
import { Product } from './product';

export abstract class BaseProductTag {
  constructor(product: Product, value: string) {
    this.product = product;
    this.value = value;
  }

  @ManyToOne({ primary: true })
  product: Product;

  @PrimaryKey({ index: true })
  value: string;

  @Property()
  obsolete = false;
}
