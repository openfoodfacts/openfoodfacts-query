import {
  Collection,
  Entity,
  ManyToOne,
  OneToMany,
  PrimaryKey,
  Property,
} from '@mikro-orm/core';
import { Product } from './product';

@Entity()
export class ProductIngredient {
  @ManyToOne({ primary: true, onDelete: 'cascade' })
  product: Product;

  @PrimaryKey()
  sequence: string;

  @ManyToOne({ index: true })
  parent?: ProductIngredient;

  @Property()
  ingredientText?: string;

  @Property()
  id?: string;

  @Property()
  ciqualFoodCode?: string;

  @Property({ type: 'double' })
  percentMin?: number;

  @Property()
  percent?: string;

  @Property({ type: 'double' })
  percentMax?: number;

  @Property({ type: 'double' })
  percentEstimate?: number;

  @Property({ type: 'json', columnType: 'json' })
  data?: any;

  @OneToMany(() => ProductIngredient, (e) => e.parent)
  ingredients = new Collection<ProductIngredient>(this);

  @Property()
  obsolete = false;
}
