import { Entity } from '@mikro-orm/core';
import { ProductTagMap } from './product-tag-map';

export function ProductTag(name: string) {
  return function (target) {
    ProductTagMap.mapTag(name, target);
    Entity()(target);
  };
}
