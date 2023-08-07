import { Entity } from '@mikro-orm/core';
import { BaseProductTag } from './base-product-tag';

@Entity()
export class ProductNutritionGradesTag extends BaseProductTag { }
@Entity()
export class ProductEcoscoreTag extends BaseProductTag { }
@Entity()
export class ProductCountriesTag extends BaseProductTag { }
@Entity()
export class ProductBrandsTag extends BaseProductTag { }
@Entity()
export class ProductCategoriesTag extends BaseProductTag { }
@Entity()
export class ProductLabelsTag extends BaseProductTag { }
@Entity()
export class ProductPackagingTag extends BaseProductTag { }
@Entity()
export class ProductOriginsTag extends BaseProductTag { }
@Entity()
export class ProductManufacturingPlacesTag extends BaseProductTag { }
@Entity()
export class ProductEmbCodesTag extends BaseProductTag { }
@Entity()
export class ProductIngredientsTag extends BaseProductTag { }
@Entity()
export class ProductAdditivesTag extends BaseProductTag { }
@Entity()
export class ProductVitaminsTag extends BaseProductTag { }
@Entity()
export class ProductMineralsTag extends BaseProductTag { }
@Entity()
export class ProductAminoAcidsTag extends BaseProductTag { }
@Entity()
export class ProductNucleotidesTag extends BaseProductTag { }
@Entity()
export class ProductAllergensTag extends BaseProductTag { }
@Entity()
export class ProductTracesTag extends BaseProductTag { }
@Entity()
export class ProductNovaGroupsTag extends BaseProductTag { }
@Entity()
export class ProductLanguagesTag extends BaseProductTag { }
@Entity()
export class ProductCreatorTag extends BaseProductTag { }
@Entity()
export class ProductEditorsTag extends BaseProductTag { }
@Entity()
export class ProductStatesTag extends BaseProductTag { }
@Entity()
export class ProductEntryDatesTag extends BaseProductTag { }
@Entity()
export class ProductLastEditDatesTag extends BaseProductTag { }
@Entity()
export class ProductCodesTag extends BaseProductTag { }
@Entity()
export class ProductNutrientLevelsTag extends BaseProductTag { }
@Entity()
export class ProductStoresTag extends BaseProductTag { }
@Entity()
export class ProductInformersTag extends BaseProductTag { }
@Entity()
export class ProductPhotographersTag extends BaseProductTag { }
@Entity()
export class ProductCheckersTag extends BaseProductTag { }
@Entity()
export class ProductCorrectorsTag extends BaseProductTag { }
@Entity()
export class ProductIngredientsFromPalmOilTag extends BaseProductTag { }
@Entity()
export class ProductIngredientsThatMayBeFromPalmOilTag extends BaseProductTag { }
@Entity()
export class ProductPurchasePlacesTag extends BaseProductTag { }
@Entity()
export class ProductIngredientsNTag extends BaseProductTag { }
@Entity()
export class ProductPnnsGroups1Tag extends BaseProductTag { }
@Entity()
export class ProductPnnsGroups2Tag extends BaseProductTag { }
@Entity()
export class ProductMiscTag extends BaseProductTag { }
@Entity()
export class ProductQualityTag extends BaseProductTag { }
@Entity()
export class ProductUnknownNutrientsTag extends BaseProductTag { }
@Entity()
export class ProductLastImageDatesTag extends BaseProductTag { }
@Entity()
export class ProductCitiesTag extends BaseProductTag { }
@Entity()
export class ProductIngredientsAnalysisTag extends BaseProductTag { }
@Entity()
export class ProductPopularityTag extends BaseProductTag { }
@Entity()
export class ProductDataSourcesTag extends BaseProductTag { }
@Entity()
export class ProductDataQualityTag extends BaseProductTag { }
@Entity()
export class ProductDataQualityBugsTag extends BaseProductTag { }
@Entity()
export class ProductDataQualityInfoTag extends BaseProductTag { }
@Entity()
export class ProductDataQualityWarningsTag extends BaseProductTag { }
@Entity()
export class ProductDataQualityErrorsTag extends BaseProductTag { }
@Entity()
export class ProductTeamsTag extends BaseProductTag { }
@Entity()
export class ProductCategoriesPropertiesTag extends BaseProductTag { }
@Entity()
export class ProductFoodGroupsTag extends BaseProductTag { }
@Entity()
export class ProductWeighersTag extends BaseProductTag { }

export const TAG_MAPPINGS = {
  countries_tags: ProductCountriesTag,
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
  allergens_tags: ProductAllergensTag,
  traces_tags: ProductTracesTag,
  nova_groups_tags: ProductNovaGroupsTag,
  nutrition_grades_tags: ProductNutritionGradesTag,
  languages_tags: ProductLanguagesTag,
  creator_tags: ProductCreatorTag,
  editors_tags: ProductEditorsTag,
  states_tags: ProductStatesTag,
  entry_dates_tags: ProductEntryDatesTag,
  last_edit_dates_tags: ProductLastEditDatesTag,
  codes_tags: ProductCodesTag,
  nutrient_levels_tags: ProductNutrientLevelsTag,
  stores_tags: ProductStoresTag,
  informers_tags: ProductInformersTag,
  photographers_tags: ProductPhotographersTag,
  checkers_tags: ProductCheckersTag,
  correctors_tags: ProductCorrectorsTag,
  ingredients_from_palm_oil_tags: ProductIngredientsFromPalmOilTag,
  ingredients_that_may_be_from_palm_oil_tags:
    ProductIngredientsThatMayBeFromPalmOilTag,
  purchase_places_tags: ProductPurchasePlacesTag,
  ingredients_n_tags: ProductIngredientsNTag,
  pnns_groups_1_tags: ProductPnnsGroups1Tag,
  pnns_groups_2_tags: ProductPnnsGroups2Tag,
  misc_tags: ProductMiscTag,
  quality_tags: ProductQualityTag,
  unknown_nutrients_tags: ProductUnknownNutrientsTag,
  last_image_dates_tags: ProductLastImageDatesTag,
  cities_tags: ProductCitiesTag,
  ingredients_analysis_tags: ProductIngredientsAnalysisTag,
  popularity_tags: ProductPopularityTag,
  data_sources_tags: ProductDataSourcesTag,
  data_quality_tags: ProductDataQualityTag,
  data_quality_bugs_tags: ProductDataQualityBugsTag,
  data_quality_info_tags: ProductDataQualityInfoTag,
  data_quality_warnings_tags: ProductDataQualityWarningsTag,
  data_quality_errors_tags: ProductDataQualityErrorsTag,
  teams_tags: ProductTeamsTag,
  categories_properties_tags: ProductCategoriesPropertiesTag,
  ecoscore_tags: ProductEcoscoreTag,
  food_groups_tags: ProductFoodGroupsTag,
  weighers_tags: ProductWeighersTag,
  // TODO: Other Nutritional Substances
};
