import { Entity, PrimaryKey, Property } from '@mikro-orm/core';
import { ProductSource } from '../enums/product-source';

@Entity()
export class Product {
  @PrimaryKey({ columnType: 'serial' })
  id: number;

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

  @Property({ columnType: 'timestamptz' })
  lastUpdated?: Date;

  @Property({ index: true })
  creator?: string;

  @Property({ index: true })
  ownersTags?: string;

  @Property()
  ingredientsWithoutCiqualCodesCount?: number;

  @Property()
  ingredientsCount?: number;

  // The following fields are populated by the query service
  @Property()
  obsolete? = false;

  // Note need to switch to xid8 when we upgrade PostgreSQL
  @Property({ columnType: 'bigint', index: true })
  processId?: bigint;

  // This is the last time off-query received the data
  @Property({ columnType: 'timestamptz' })
  lastProcessed?: Date;

  @Property()
  source?: ProductSource;

  @Property()
  revision?: number;
}

export const MAPPED_FIELDS = [
  'code',
  'product_name',
  'creator',
  'owners_tags',
  'last_modified_t', // Note we actually use last_updated_t for checks but not all products may have this
  'last_updated_t',
  'ingredients_n',
  'ingredients_without_ciqual_codes_n',
  'ingredients',
  'rev',
];

export function normalizeCode(code: string) {
  // Logic re-created from https://github.com/openfoodfacts/openfoodfacts-server/blob/main/lib/ProductOpener/Products.pm#L313
  // Return the code as-is if it is not all digits
  if (!/^\d+$/.test(code)) return code;

  // Remove leading zeroes
  code = code.replace(/^0+/, '');

  // Add leading zeroes to have at least 13 digits
  if (code.length < 13) code = code.padStart(13, '0');

  // Remove leading zeroes for EAN8s to keep only 8 digits
  if (code.length === 13 && code.startsWith('00000')) code = code.substring(5);

  return code;
}
