/* eslint-disable prettier/prettier */
import { Migration } from '@mikro-orm/migrations';
import { SCHEMA, VIEW_PASSWORD, VIEW_USER } from '../constants';

export class Migration20240719101700Redis extends Migration {
  async up(): Promise<void> {
    this.addSql(`CREATE TABLE IF NOT EXISTS query.product_update_event (id text NOT NULL PRIMARY KEY, updated_at timestamptz NOT NULL, code text NULL, message jsonb NOT NULL)`);
    this.addSql(`CREATE USER ${VIEW_USER} PASSWORD '${VIEW_PASSWORD}'`);
    this.addSql(`ALTER ROLE ${VIEW_USER} SET search_path=${SCHEMA},public`,
    );
    this.addSql(`GRANT USAGE ON SCHEMA ${SCHEMA} TO ${VIEW_USER}`);

    this.addSql(`CREATE OR REPLACE VIEW product_update_view AS SELECT 
        DATE_TRUNC('day', pe.updated_at) updated_day,
        p.owners_tags,
        count(*) update_count,
        count(DISTINCT pe.code) product_count
    FROM product_update_event pe
        LEFT JOIN product p on p.code = pe.code
    GROUP BY DATE_TRUNC('day', pe.updated_at),
        p.owners_tags`);
    this.addSql(`GRANT SELECT ON product_update_view TO ${VIEW_USER}`);
  }
}
