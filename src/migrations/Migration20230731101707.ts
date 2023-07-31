import { Migration } from '@mikro-orm/migrations';

export class Migration20230731101707 extends Migration {

  async up(): Promise<void> {
    this.addSql('create table "off"."product_ecoscore_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_ecoscore_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('create table "off"."product_nutrition_grades_tag" ("product_id" uuid not null, "value" text not null, "sequence" int not null, constraint "product_nutrition_grades_tag_pkey" primary key ("product_id", "value", "sequence"));');

    this.addSql('alter table "off"."product_ecoscore_tag" add constraint "product_ecoscore_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('alter table "off"."product_nutrition_grades_tag" add constraint "product_nutrition_grades_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('drop table if exists "off"."product_tag" cascade;');
  }

  async down(): Promise<void> {
    this.addSql('create table "off"."product_tag" ("product_id" uuid not null, "tag_type" text not null, "sequence" int not null, "value" text not null, constraint "product_tag_pkey" primary key ("product_id", "tag_type", "sequence"));');
    this.addSql('create index "product_tag_tag_type_value_product_id_index" on "off"."product_tag" ("tag_type", "value", "product_id");');

    this.addSql('alter table "off"."product_tag" add constraint "product_tag_product_id_foreign" foreign key ("product_id") references "off"."product" ("id") on update cascade;');

    this.addSql('drop table if exists "off"."product_ecoscore_tag" cascade;');

    this.addSql('drop table if exists "off"."product_nutrition_grades_tag" cascade;');
  }

}
