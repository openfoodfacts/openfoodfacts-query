import { Migration } from '@mikro-orm/migrations';

export class Migration20230904095811 extends Migration {

  async up(): Promise<void> {
    this.addSql('alter table "query"."product_additives_tag" drop constraint "product_additives_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_allergens_tag" drop constraint "product_allergens_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_amino_acids_tag" drop constraint "product_amino_acids_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_brands_tag" drop constraint "product_brands_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_categories_tag" drop constraint "product_categories_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_countries_tag" drop constraint "product_countries_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_data_sources_tag" drop constraint "product_data_sources_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_ecoscore_tag" drop constraint "product_ecoscore_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_emb_codes_tag" drop constraint "product_emb_codes_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_entry_dates_tag" drop constraint "product_entry_dates_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_ingredients_tag" drop constraint "product_ingredients_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_labels_tag" drop constraint "product_labels_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_languages_tag" drop constraint "product_languages_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_last_check_dates_tag" drop constraint "product_last_check_dates_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_last_edit_dates_tag" drop constraint "product_last_edit_dates_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_manufacturing_places_tag" drop constraint "product_manufacturing_places_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_minerals_tag" drop constraint "product_minerals_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_misc_tag" drop constraint "product_misc_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_nova_groups_tag" drop constraint "product_nova_groups_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_nucleotides_tag" drop constraint "product_nucleotides_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_nutrition_grades_tag" drop constraint "product_nutrition_grades_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_origins_tag" drop constraint "product_origins_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_other_nutritional_substances_tag" drop constraint "product_other_nutritional_substances_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_packaging_tag" drop constraint "product_packaging_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_states_tag" drop constraint "product_states_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_teams_tag" drop constraint "product_teams_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_traces_tag" drop constraint "product_traces_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_vitamins_tag" drop constraint "product_vitamins_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_additives_tag" add constraint "product_additives_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_allergens_tag" add constraint "product_allergens_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_amino_acids_tag" add constraint "product_amino_acids_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_brands_tag" add constraint "product_brands_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_categories_tag" add constraint "product_categories_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_countries_tag" add constraint "product_countries_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_data_sources_tag" add constraint "product_data_sources_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_ecoscore_tag" add constraint "product_ecoscore_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_emb_codes_tag" add constraint "product_emb_codes_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_entry_dates_tag" add constraint "product_entry_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_ingredients_tag" add constraint "product_ingredients_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_labels_tag" add constraint "product_labels_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_languages_tag" add constraint "product_languages_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_last_check_dates_tag" add constraint "product_last_check_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_minerals_tag" add constraint "product_minerals_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_misc_tag" add constraint "product_misc_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_nova_groups_tag" add constraint "product_nova_groups_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_nucleotides_tag" add constraint "product_nucleotides_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_origins_tag" add constraint "product_origins_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_other_nutritional_substances_tag" add constraint "product_other_nutritional_substances_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_packaging_tag" add constraint "product_packaging_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_states_tag" add constraint "product_states_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_teams_tag" add constraint "product_teams_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_traces_tag" add constraint "product_traces_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');

    this.addSql('alter table "query"."product_vitamins_tag" add constraint "product_vitamins_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade on delete cascade;');
  }

  async down(): Promise<void> {
    this.addSql('alter table "query"."product_additives_tag" drop constraint "product_additives_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_allergens_tag" drop constraint "product_allergens_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_amino_acids_tag" drop constraint "product_amino_acids_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_brands_tag" drop constraint "product_brands_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_categories_tag" drop constraint "product_categories_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_countries_tag" drop constraint "product_countries_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_data_sources_tag" drop constraint "product_data_sources_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_ecoscore_tag" drop constraint "product_ecoscore_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_emb_codes_tag" drop constraint "product_emb_codes_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_entry_dates_tag" drop constraint "product_entry_dates_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_ingredients_tag" drop constraint "product_ingredients_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_labels_tag" drop constraint "product_labels_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_languages_tag" drop constraint "product_languages_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_last_check_dates_tag" drop constraint "product_last_check_dates_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_last_edit_dates_tag" drop constraint "product_last_edit_dates_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_manufacturing_places_tag" drop constraint "product_manufacturing_places_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_minerals_tag" drop constraint "product_minerals_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_misc_tag" drop constraint "product_misc_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_nova_groups_tag" drop constraint "product_nova_groups_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_nucleotides_tag" drop constraint "product_nucleotides_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_nutrition_grades_tag" drop constraint "product_nutrition_grades_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_origins_tag" drop constraint "product_origins_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_other_nutritional_substances_tag" drop constraint "product_other_nutritional_substances_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_packaging_tag" drop constraint "product_packaging_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_states_tag" drop constraint "product_states_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_teams_tag" drop constraint "product_teams_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_traces_tag" drop constraint "product_traces_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_vitamins_tag" drop constraint "product_vitamins_tag_product_id_foreign";');

    this.addSql('alter table "query"."product_additives_tag" add constraint "product_additives_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_allergens_tag" add constraint "product_allergens_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_amino_acids_tag" add constraint "product_amino_acids_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_brands_tag" add constraint "product_brands_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_categories_tag" add constraint "product_categories_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_countries_tag" add constraint "product_countries_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_data_sources_tag" add constraint "product_data_sources_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_ecoscore_tag" add constraint "product_ecoscore_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_emb_codes_tag" add constraint "product_emb_codes_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_entry_dates_tag" add constraint "product_entry_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_ingredients_tag" add constraint "product_ingredients_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_labels_tag" add constraint "product_labels_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_languages_tag" add constraint "product_languages_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_last_check_dates_tag" add constraint "product_last_check_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_last_edit_dates_tag" add constraint "product_last_edit_dates_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_manufacturing_places_tag" add constraint "product_manufacturing_places_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_minerals_tag" add constraint "product_minerals_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_misc_tag" add constraint "product_misc_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_nova_groups_tag" add constraint "product_nova_groups_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_nucleotides_tag" add constraint "product_nucleotides_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_origins_tag" add constraint "product_origins_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_other_nutritional_substances_tag" add constraint "product_other_nutritional_substances_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_packaging_tag" add constraint "product_packaging_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_states_tag" add constraint "product_states_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_teams_tag" add constraint "product_teams_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_traces_tag" add constraint "product_traces_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');

    this.addSql('alter table "query"."product_vitamins_tag" add constraint "product_vitamins_tag_product_id_foreign" foreign key ("product_id") references "query"."product" ("id") on update cascade;');
  }

}
