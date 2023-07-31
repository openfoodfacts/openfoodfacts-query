import { Entity } from '@mikro-orm/core';
import { BaseProductTag } from './base-product-tag';

@Entity()
export class ProductNutritionGradesTag extends BaseProductTag { }

@Entity()
export class ProductEcoscoreTag extends BaseProductTag { }

export const TAG_MAPPINGS = {
  nutrition_grades_tags: ProductNutritionGradesTag,
  ecoscore_tags: ProductEcoscoreTag,
};
