import { Entity, PrimaryKey, Property } from '@mikro-orm/core';
import { Ulid } from 'id128';
import { ProductSource } from '../enums/product-source';

@Entity()
export class Product {
  @PrimaryKey({ type: 'uuid' })
  id = Ulid.generate().toRaw();

  /** The full JSON structure retreived from Product Opener */
  @Property({ type: 'json', columnType: 'json' })
  data?: any;

  // The following fields map directly to Product fields
  @Property()
  name?: string;

  // @Index({ type: 'fulltext' })
  // @Property<Product>({
  //   type: FullTextType,
  //   onUpdate: (e) => e.name?.replace(/\?/g, ''),
  // }) // Question marks seem to confuse binding
  // search?: string;

  @Property({ index: true })
  code?: string;

  @Property()
  lastModified?: Date;

  @Property()
  creator?: string;

  @Property()
  ownersTags?: string;

  @Property()
  ingredientsWithoutCiqualCodesCount?: number;

  @Property()
  ingredientsCount?: number;

  // The followign fields are populated by the query service
  @Property()
  obsolete = false;

  @Property({ type: 'uuid', index: true })
  lastUpdateId?: string;

  @Property()
  lastUpdated?: Date;

  @Property()
  source?: ProductSource;
}

export const MAPPED_FIELDS = [
  'code',
  'product_name',
  'creator',
  'owners_tags',
  'last_modified_t',
  'ingredients_n',
  'ingredients_without_ciqual_codes_n',
  'ingredients',
];
