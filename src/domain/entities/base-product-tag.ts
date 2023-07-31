import { ManyToOne, PrimaryKey } from '@mikro-orm/core';
import { Product } from './product';

export abstract class BaseProductTag {
  constructor(product: Product, sequence: number, value: string) {
    this.product = product;
    this.sequence = sequence;
    this.value = value;
  }

  @ManyToOne({ primary: true })
  product: Product;

  @PrimaryKey()
  value: string;

  @PrimaryKey()
  sequence: number;
}
