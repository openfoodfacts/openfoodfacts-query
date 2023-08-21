import {
  Collection,
  Entity,
  Index,
  OneToMany,
  PrimaryKey,
  Property,
} from '@mikro-orm/core';
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

  @Property({ type: 'uuid', index: true })
  lastUpdateId?: string;

  @Property()
  obsolete = false;
}

export const MAPPED_FIELDS = [
  'code',
  'product_name',
  'ingredients_text',
  'nutrition_data_per',
  'nutrition_data_prepared_per',
  'serving_quantity',
  'serving_size',
  'creator',
  'owners_tags',
  'last_modified_t',
];
