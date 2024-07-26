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
  
    this.addSql(`CREATE TYPE action AS ENUM ('created', 'updated', 'archived', 'unarchived', 'deleted', 'unknown')`);

    this.addSql(`CREATE TABLE IF NOT EXISTS product_action (
	    product_id int,
      updated_date date,
      action action,
      contributor_id int,
      update_count int,
     constraint product_action_pkey primary key (updated_date, product_id, action, contributor_id))`);

    this.addSql(`CREATE USER ${VIEW_USER} PASSWORD '${VIEW_PASSWORD}'`);
    this.addSql(`ALTER ROLE ${VIEW_USER} SET search_path=${SCHEMA},public`);
    this.addSql(`GRANT USAGE ON SCHEMA ${SCHEMA} TO ${VIEW_USER}`);
    this.addSql(`GRANT SELECT ON product_action TO ${VIEW_USER}`);
    this.addSql(`GRANT SELECT ON product TO ${VIEW_USER}`);
  }
}
