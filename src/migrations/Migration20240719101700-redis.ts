/* eslint-disable prettier/prettier */
import { Migration } from '@mikro-orm/migrations';
import { VIEW_PASSWORD, VIEW_USER } from '../constants';

export class Migration20240719101700Redis extends Migration {
  async up(): Promise<void> {
    this.addSql(`CREATE TABLE IF NOT EXISTS query.product_update_event (id text NOT NULL PRIMARY KEY, updated_at timestamptz NOT NULL, code text NULL, message jsonb NOT NULL)`);
    this.addSql(`CREATE USER ${VIEW_USER} PASSWORD '${VIEW_PASSWORD}'`);
  }
}
