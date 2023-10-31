import { Migration } from '@mikro-orm/migrations';

export class Migration20231030101011 extends Migration {
  async up(): Promise<void> {
    this.addSql(
      'create table "query"."loaded_tag" ("id" text not null, constraint "loaded_tag_pkey" primary key ("id"));',
    );
    this.addSql(
      `insert into "query"."loaded_tag" ("id") values ('countries_tags'),('nutrition_grades_tags'),('nova_groups_tags'),('ecoscore_tags'),('brands_tags'),('categories_tags'),('labels_tags'),('packaging_tags'),('origins_tags'),('manufacturing_places_tags'),('emb_codes_tags'),('ingredients_tags'),('additives_tags'),('vitamins_tags'),('minerals_tags'),('amino_acids_tags'),('nucleotides_tags'),('other_nutritional_substances_tags'),('allergens_tags'),('traces_tags'),('misc_tags'),('languages_tags'),('states_tags'),('data_sources_tags'),('entry_dates_tags'),('last_edit_dates_tags'),('last_check_dates_tags'),('teams_tags') on conflict do nothing;`,
    );
  }

  async down(): Promise<void> {
    this.addSql('drop table if exists "query"."loaded_tag" cascade;');
  }
}
