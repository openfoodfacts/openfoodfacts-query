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
@ProductTag('data_quality_errors_tags')
export class ProductDataQualityErrorsTag extends BaseProductTag {}
@ProductTag('data_quality_tags')
export class ProductDataQualityTag extends BaseProductTag {}
@ProductTag('editors_tags')
export class ProductEditorsTag extends BaseProductTag {}
@ProductTag('stores_tags')
export class ProductStoresTag extends BaseProductTag {}
@ProductTag('ingredients_original_tags')
export class ProductIngredientsOriginalTag extends BaseProductTag {}

// From Issue #22
@ProductTag('checkers_tags')
export class ProductCheckersTag extends BaseProductTag {}
@ProductTag('cities_tags')
export class ProductCitiesTag extends BaseProductTag {}
@ProductTag('correctors_tags')
export class ProductCorrectorsTag extends BaseProductTag {}
@ProductTag('debug_tags')
export class ProductDebugTag extends BaseProductTag {}
@ProductTag('informers_tags')
export class ProductInformersTag extends BaseProductTag {}
@ProductTag('ingredients_from_palm_oil_tags')
export class ProductIngredientsFromPalmOilTag extends BaseProductTag {}
@ProductTag('ingredients_that_may_be_from_palm_oil_tags')
export class ProductIngredientsThatMayBeFromPalmOilTag extends BaseProductTag {}
// Not found in PO
//@ProductTag('known_nutrients')
//export class Product Tag extends BaseProductTag {}
@ProductTag('last_image_dates_tags')
export class ProductLatestImageDatesTag extends BaseProductTag {}
@ProductTag('ingredients_n_tags')
export class ProductIngredientsNTag extends BaseProductTag {}
@ProductTag('nutrient_levels_tags')
export class ProductNutrientLevelsTag extends BaseProductTag {}
// This is a hash
//@ProductTag('packager_codes')
//export class Product Tag extends BaseProductTag {}
@ProductTag('periods_after_opening_tags')
export class ProductPeriodsAfterOpeningTag extends BaseProductTag {}
@ProductTag('photographers_tags')
export class ProductPhotographersTag extends BaseProductTag {}
@ProductTag('pnns_groups_1_tags')
export class ProductPnnsGroups1Tag extends BaseProductTag {}
@ProductTag('pnns_groups_2_tags')
export class ProductPnnsGroups2Tag extends BaseProductTag {}
@ProductTag('purchase_places_tags')
export class ProductPurchasePlacesTag extends BaseProductTag {}
@ProductTag('unknown_nutrients_tags')
export class ProductUnknownNutrientsTag extends BaseProductTag {}
// Thing this is editors
//@ProductTag('contributors')
//export class Product Tag extends BaseProductTag {}
@ProductTag('popularity_tags')
export class ProductPopularityTag extends BaseProductTag {}
@ProductTag('ingredients_analysis_tags')
export class ProductIngredientsAnalysisTag extends BaseProductTag {}
@ProductTag('data_quality_bugs_tags')
export class ProductDataQualityBugsTag extends BaseProductTag {}
@ProductTag('data_quality_warnings_tags')
export class ProductDataQualityWarningsTag extends BaseProductTag {}
// Can;t see these in PO
//@ProductTag('data_quality_warnings_producers')
//export class Product Tag extends BaseProductTag {}
//@ProductTag('data_quality_errors_producers')
//export class Product Tag extends BaseProductTag {}
//@ProductTag('possible_improvements')
//export class Product Tag extends BaseProductTag {}
//@ProductTag('imports')
//export class Product Tag extends BaseProductTag {}
@ProductTag('categories_properties_tags')
export class ProductCategoriesProperitesTag extends BaseProductTag {}
// This is a scalar
//@ProductTag('owners_tags')
//export class ProductOwnersTag extends BaseProductTag {}
@ProductTag('food_groups_tags')
export class ProductFoodGroupsTag extends BaseProductTag {}
@ProductTag('weighers_tags')
export class ProductWeighersTag extends BaseProductTag {}
@ProductTag('packaging_shapes_tags')
export class ProductPackagingShapesTag extends BaseProductTag {}
@ProductTag('packaging_materials_tags')
export class ProductPackagingMaterialsTag extends BaseProductTag {}
@ProductTag('packaging_recycling_tags')
export class ProductPackagingRecyclingTag extends BaseProductTag {}
@ProductTag('nutriscore_tags')
export class ProductNutriscoreTag extends BaseProductTag {}
@ProductTag('nutriscore_2021_tags')
export class ProductNutriscore2021Tag extends BaseProductTag {}
@ProductTag('nutriscore_2023_tags')
export class ProductNutriscore2023Tag extends BaseProductTag {}

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
