import {
  Collection,
  Entity,
  Index,
  OneToMany,
  PrimaryKey,
  Property,
} from '@mikro-orm/core';
import { ProductTag } from './product-tag';
import { Ulid } from 'id128';
import { FullTextType } from '@mikro-orm/postgresql';

@Entity()
export class Product {
  @PrimaryKey({ type: 'uuid' })
  id = Ulid.generate().toRaw();

  @Property({ type: 'jsonb' })
  data?: any;

  @Property()
  name?: string;

  @Index({ type: 'fulltext' })
  @Property<Product>({
    type: FullTextType,
    onUpdate: (e) => e.name?.replace(/\?/g, ''),
  }) // Question marks seem to confuse binding
  search?: string;

  @Property({ index: true })
  code?: string;

  @Property()
  ingredientsText?: string;

  @Property()
  nutritionAsSoldPer?: string;

  @Property()
  nutritionPreparedPer?: string;

  @Property()
  servingSize?: string;

  @Property({ type: 'double' })
  servingQuantity?: number;

  @Property()
  lastModified?: Date;

  @Property()
  creator?: string;

  @Property()
  ownersTags?: string;

  @OneToMany(() => ProductTag, (e) => e.product)
  tags = new Collection<ProductTag>(this);
}
