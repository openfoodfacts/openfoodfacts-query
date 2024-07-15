import { Migration } from '@mikro-orm/migrations';
import { SCHEMA } from '../constants';

export class Migration20240712165000SearchPath extends Migration {
  async up(): Promise<void> {
    // Merged in from a later migration
    this.addSql(
      `ALTER ROLE ${process.env.POSTGRES_USER} SET search_path=${SCHEMA},public`,
    );
  }
}
