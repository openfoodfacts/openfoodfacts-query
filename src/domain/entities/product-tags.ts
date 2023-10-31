import { Entity } from '@mikro-orm/core';
import { BaseProductTag } from './base-product-tag';

@Entity()
export class ProductCountriesTag extends BaseProductTag {}
@Entity()
export class ProductNutritionGradesTag extends BaseProductTag {}
@Entity()
export class ProductNovaGroupsTag extends BaseProductTag {}
@Entity()
export class ProductEcoscoreTag extends BaseProductTag {}
@Entity()
export class ProductBrandsTag extends BaseProductTag {}
@Entity()
export class ProductCategoriesTag extends BaseProductTag {}
@Entity()
export class ProductLabelsTag extends BaseProductTag {}
@Entity()
export class ProductPackagingTag extends BaseProductTag {}
@Entity()
export class ProductOriginsTag extends BaseProductTag {}
@Entity()
export class ProductManufacturingPlacesTag extends BaseProductTag {}
@Entity()
export class ProductEmbCodesTag extends BaseProductTag {}
@Entity()
export class ProductIngredientsTag extends BaseProductTag {}
@Entity()
export class ProductAdditivesTag extends BaseProductTag {}
@Entity()
export class ProductVitaminsTag extends BaseProductTag {}
@Entity()
export class ProductMineralsTag extends BaseProductTag {}
@Entity()
export class ProductAminoAcidsTag extends BaseProductTag {}
@Entity()
export class ProductNucleotidesTag extends BaseProductTag {}
@Entity()
export class ProductOtherNutritionalSubstancesTag extends BaseProductTag {}
@Entity()
export class ProductAllergensTag extends BaseProductTag {}
@Entity()
export class ProductTracesTag extends BaseProductTag {}
@Entity()
export class ProductMiscTag extends BaseProductTag {}
@Entity()
export class ProductLanguagesTag extends BaseProductTag {}
@Entity()
export class ProductStatesTag extends BaseProductTag {}
@Entity()
export class ProductDataSourcesTag extends BaseProductTag {}
@Entity()
export class ProductEntryDatesTag extends BaseProductTag {}
@Entity()
export class ProductLastEditDatesTag extends BaseProductTag {}
@Entity()
export class ProductLastCheckDatesTag extends BaseProductTag {}
@Entity()
export class ProductTeamsTag extends BaseProductTag {}
@Entity()
export class ProductKeywordsTag extends BaseProductTag {}
@Entity()
export class ProductCodesTag extends BaseProductTag {}
@Entity()
export class ProductDataQualityErrorsTag extends BaseProductTag {}
@Entity()
export class ProductDataQualityTag extends BaseProductTag {}
@Entity()
export class ProductEditorsTag extends BaseProductTag {}
@Entity()
export class ProductStoresTag extends BaseProductTag {}
@Entity()
export class ProductIngredientsOriginalTag extends BaseProductTag {}

/* From Config_off.pm
# fields for drilldown facet navigation

@drilldown_fields = qw(
  nutrition_grades
  nova_groups
  ecoscore
  brands
  categories
  labels
  packaging
  origins
  manufacturing_places
  emb_codes
  ingredients
  additives
  vitamins
  minerals
  amino_acids
  nucleotides
  other_nutritional_substances
  allergens
  traces
  misc
  languages
  users
  states
  data_sources
  entry_dates
  last_edit_dates
  last_check_dates
  teams
);
*/

export const MAPPED_TAGS = {
  countries_tags: ProductCountriesTag,
  nutrition_grades_tags: ProductNutritionGradesTag,
  nova_groups_tags: ProductNovaGroupsTag,
  ecoscore_tags: ProductEcoscoreTag,
  brands_tags: ProductBrandsTag,
  categories_tags: ProductCategoriesTag,
  labels_tags: ProductLabelsTag,
  packaging_tags: ProductPackagingTag,
  origins_tags: ProductOriginsTag,
  manufacturing_places_tags: ProductManufacturingPlacesTag,
  emb_codes_tags: ProductEmbCodesTag,
  ingredients_tags: ProductIngredientsTag,
  additives_tags: ProductAdditivesTag,
  vitamins_tags: ProductVitaminsTag,
  minerals_tags: ProductMineralsTag,
  amino_acids_tags: ProductAminoAcidsTag,
  nucleotides_tags: ProductNucleotidesTag,
  other_nutritional_substances_tags: ProductOtherNutritionalSubstancesTag,
  allergens_tags: ProductAllergensTag,
  traces_tags: ProductTracesTag,
  misc_tags: ProductMiscTag,
  languages_tags: ProductLanguagesTag,
  states_tags: ProductStatesTag,
  data_sources_tags: ProductDataSourcesTag,
  entry_dates_tags: ProductEntryDatesTag,
  last_edit_dates_tags: ProductLastEditDatesTag,
  last_check_dates_tags: ProductLastCheckDatesTag,
  teams_tags: ProductTeamsTag,
  // Added later
  _keywords: ProductKeywordsTag,
  codes_tags: ProductCodesTag,
  data_quality_tags: ProductDataQualityTag,
  data_quality_errors_tags: ProductDataQualityErrorsTag,
  editors_tags: ProductEditorsTag,
  stores_tags: ProductStoresTag,
  ingredients_original_tags: ProductIngredientsOriginalTag,
};
