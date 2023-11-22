import { BaseProductTag } from './base-product-tag';
import { ProductTag } from './product-tag';

@ProductTag('countries_tags')
export class ProductCountriesTag extends BaseProductTag {}
@ProductTag('nutrition_grades_tags')
export class ProductNutritionGradesTag extends BaseProductTag {}
@ProductTag('nova_groups_tags')
export class ProductNovaGroupsTag extends BaseProductTag {}
@ProductTag('ecoscore_tags')
export class ProductEcoscoreTag extends BaseProductTag {}
@ProductTag('brands_tags')
export class ProductBrandsTag extends BaseProductTag {}
@ProductTag('categories_tags')
export class ProductCategoriesTag extends BaseProductTag {}
@ProductTag('labels_tags')
export class ProductLabelsTag extends BaseProductTag {}
@ProductTag('packaging_tags')
export class ProductPackagingTag extends BaseProductTag {}
@ProductTag('origins_tags')
export class ProductOriginsTag extends BaseProductTag {}
@ProductTag('manufacturing_places_tags')
export class ProductManufacturingPlacesTag extends BaseProductTag {}
@ProductTag('emb_codes_tags')
export class ProductEmbCodesTag extends BaseProductTag {}
@ProductTag('ingredients_tags')
export class ProductIngredientsTag extends BaseProductTag {}
@ProductTag('additives_tags')
export class ProductAdditivesTag extends BaseProductTag {}
@ProductTag('vitamins_tags')
export class ProductVitaminsTag extends BaseProductTag {}
@ProductTag('minerals_tags')
export class ProductMineralsTag extends BaseProductTag {}
@ProductTag('amino_acids_tags')
export class ProductAminoAcidsTag extends BaseProductTag {}
@ProductTag('nucleotides_tags')
export class ProductNucleotidesTag extends BaseProductTag {}
@ProductTag('other_nutritional_substances_tags')
export class ProductOtherNutritionalSubstancesTag extends BaseProductTag {}
@ProductTag('allergens_tags')
export class ProductAllergensTag extends BaseProductTag {}
@ProductTag('traces_tags')
export class ProductTracesTag extends BaseProductTag {}
@ProductTag('misc_tags')
export class ProductMiscTag extends BaseProductTag {}
@ProductTag('languages_tags')
export class ProductLanguagesTag extends BaseProductTag {}
@ProductTag('states_tags')
export class ProductStatesTag extends BaseProductTag {}
@ProductTag('data_sources_tags')
export class ProductDataSourcesTag extends BaseProductTag {}
@ProductTag('entry_dates_tags')
export class ProductEntryDatesTag extends BaseProductTag {}
@ProductTag('last_edit_dates_tags')
export class ProductLastEditDatesTag extends BaseProductTag {}
@ProductTag('last_check_dates_tags')
export class ProductLastCheckDatesTag extends BaseProductTag {}
// Don't use Teams for query tests as we delete the loaded tag in the Import tests
@ProductTag('teams_tags')
export class ProductTeamsTag extends BaseProductTag {}
@ProductTag('_keywords')
export class ProductKeywordsTag extends BaseProductTag {}
@ProductTag('codes_tags')
export class ProductCodesTag extends BaseProductTag {}
@ProductTag('data_quality_tags')
export class ProductDataQualityErrorsTag extends BaseProductTag {}
@ProductTag('data_quality_errors_tags')
export class ProductDataQualityTag extends BaseProductTag {}
@ProductTag('editors_tags')
export class ProductEditorsTag extends BaseProductTag {}
@ProductTag('stores_tags')
export class ProductStoresTag extends BaseProductTag {}
@ProductTag('ingredients_original_tags')
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
