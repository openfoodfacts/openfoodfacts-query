/* eslint-disable prettier/prettier */
import { Migration } from '@mikro-orm/migrations';
import { SCHEMA, VIEW_PASSWORD, VIEW_USER } from '../constants';

export class Migration20240719101700Redis extends Migration {
  async up(): Promise<void> {
    this.addSql(`CREATE TABLE IF NOT EXISTS product_update_event (
      id text NOT NULL PRIMARY KEY,
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
  
    this.addSql(`INSERT INTO update_type (code) VALUES ('created'), ('updated'), ('archived'), ('unarchived'), ('deleted'), ('unknown')`);

    this.addSql(`CREATE TABLE IF NOT EXISTS product_update (
	    product_id int,
      updated_date date,
      update_type_id int,
      contributor_id int,
      update_count int,
     constraint product_update_pkey primary key (updated_date, product_id, update_type_id, contributor_id))`);

    this.addSql(`CREATE USER ${VIEW_USER} PASSWORD '${VIEW_PASSWORD}'`);
    this.addSql(`ALTER ROLE ${VIEW_USER} SET search_path=${SCHEMA},public`);
    this.addSql(`GRANT USAGE ON SCHEMA ${SCHEMA} TO ${VIEW_USER}`);
    this.addSql(`GRANT SELECT ON product_update TO ${VIEW_USER}`);
    this.addSql(`GRANT SELECT ON update_type TO ${VIEW_USER}`);
    this.addSql(`GRANT SELECT ON contributor TO ${VIEW_USER}`);
    this.addSql(`GRANT SELECT ON product TO ${VIEW_USER}`);
  }
}
