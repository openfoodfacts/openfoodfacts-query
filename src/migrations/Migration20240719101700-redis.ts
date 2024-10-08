/* eslint-disable prettier/prettier */
import { Migration } from '@mikro-orm/migrations';
import { VIEW_PASSWORD, VIEW_USER } from '../constants';

export class Migration20240719101700Redis extends Migration {
  async up(): Promise<void> {
    this.addSql(`CREATE TABLE IF NOT EXISTS product_update_event (
      id bigserial NOT NULL PRIMARY KEY,
      message_id text NOT NULL,
      received_at timestamptz NOT NULL,
      updated_at timestamptz NOT NULL,
      message jsonb NOT NULL)`);

    this.addSql(`CREATE TABLE IF NOT EXISTS contributor (
      id serial,
      code text,
      constraint contributor_pkey primary key (id),
      constraint contributor_code unique (code))`);

    this.addSql(`CREATE TABLE IF NOT EXISTS update_type (
      id serial,
      code text,
      constraint action_pkey primary key (id),
      constraint action_code unique (code))`);
  
    this.addSql(`INSERT INTO update_type (code) VALUES ('created'), ('updated'), ('archived'), ('unarchived'), ('deleted'), ('reprocessed'), ('unknown')`);

    this.addSql(`CREATE TABLE IF NOT EXISTS product_update (
	    product_id int,
	    revision int,
      updated_date date,
      update_type_id int,
      contributor_id int,
      event_id bigint,
     constraint product_update_pkey primary key (product_id, revision))`);
    this.addSql('create index product_update_updated_date_index on product_update (updated_date);');

    this.addSql('create schema if not exists views;');
    this.addSql(`CREATE USER ${VIEW_USER} PASSWORD '${VIEW_PASSWORD}'`);
    this.addSql(`ALTER ROLE ${VIEW_USER} SET search_path=views,public`);
    this.addSql(`CREATE OR REPLACE VIEW views.product_updates_by_owner AS
      SELECT pu.updated_date,
        p.owners_tags owner_tag,
        ut.code update_type,
        count(*) update_count,
        count(DISTINCT pu.product_id) product_count
      FROM product_update pu
      JOIN product p ON p.id = pu.product_id
      JOIN update_type ut ON ut.id = pu.update_type_id
      GROUP BY pu.updated_date,
        p.owners_tags,
        ut.code`);
    this.addSql(`GRANT USAGE ON SCHEMA views TO ${VIEW_USER}`);
    this.addSql(`GRANT SELECT ON views.product_updates_by_owner TO ${VIEW_USER}`);
  }
  async down(): Promise<void> {
    this.addSql(`drop owned by ${VIEW_USER}`);
    this.addSql(`DROP ROLE ${VIEW_USER}`);
    this.addSql(`drop view views.product_updates_by_owner`);
    this.addSql(`drop schema views`);
    this.addSql(`drop table product_update CASCADE`);
    this.addSql(`drop table contributor CASCADE`);
    this.addSql(`drop table update_type CASCADE`);
    this.addSql(`drop table product_update_event CASCADE`);
  }
}
