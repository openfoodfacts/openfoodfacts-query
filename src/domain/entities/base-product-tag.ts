import { ManyToOne, PrimaryKey, Property } from '@mikro-orm/core';
import { Product } from './product';

export abstract class BaseProductTag {
  constructor(product: Product, value: string) {
    this.product = product;
    this.value = value;
  }

  // We put the value first so that the primary key index is optimised to search by value
  @PrimaryKey()
  value: string;

  // Still need an index on product id for deletes during imports, but product id is smaller than value
  @ManyToOne({ primary: true, onDelete: 'cascade', index: true })
  product: Product;

  @Property()
  obsolete? = false;
}
