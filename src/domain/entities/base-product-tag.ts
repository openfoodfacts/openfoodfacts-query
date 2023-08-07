import { ManyToOne, PrimaryKey, Property } from '@mikro-orm/core';
import { Product } from './product';

export abstract class BaseProductTag {
  constructor(product: Product, value: string) {
    this.product = product;
    this.value = value;
  }

  @PrimaryKey()
  value: string;

  @ManyToOne({ primary: true })
  product: Product;

  @Property()
  obsolete = false;
}
