import { Entity, PrimaryKey, Property } from '@mikro-orm/core';
import { Ulid } from 'id128';

@Entity()
export class Product {
  @PrimaryKey({ type: 'uuid' })
  id = Ulid.generate().toRaw();

  @Property({ type: 'json', columnType: 'json' })
  data?: any;

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

  @Property({ type: 'uuid', index: true })
  lastUpdateId?: string;

  @Property()
  obsolete = false;

  @Property()
  ingredientsWithoutCiqualCodesCount?: number;

  @Property()
  ingredientsCount?: number;
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
