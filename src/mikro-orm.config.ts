import { TsMorphMetadataProvider } from '@mikro-orm/reflection';
import {
  DateTimeType,
  Platform,
  TextType,
  Type,
  defineConfig,
} from '@mikro-orm/core';
import { SCHEMA } from './constants';
import { Logger } from '@nestjs/common';

class DateTimeNtzType extends DateTimeType {
  getColumnType(): string {
    return 'timestamp';
  }
}

const logger = new Logger('MikroOrm');

export default defineConfig({
  entities: ['./dist/domain/entities'],
  entitiesTs: ['./src/domain/entities'],
  metadataProvider: TsMorphMetadataProvider,
  dbName: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  host: process.env.POSTGRES_HOST,
  port: parseInt(process.env.POSTGRES_EXPOSE.split(':').pop()),
  schema: SCHEMA,
  driverOptions: {
    searchPath: [SCHEMA, 'public'],
  },
  type: 'postgresql',
  forceUtcTimezone: true,
  discovery: {
    getMappedType(type: string, platform: Platform) {
      // override the mapping for string properties only
      if (type === 'string') {
        return Type.getType(TextType);
      }
      if (type === 'datetime') {
        return new DateTimeNtzType();
      }

      const mappedType = platform.getDefaultMappedType(type);
      return mappedType;
    },
  },
  migrations: {
    path: 'dist/migrations',
    pathTs: 'src/migrations',
  },
  pool: {
    afterCreate: function (conn: any, done: any) {
      // issue a query to verify SQL connection is working
      conn.query('select 1 as result', function (err) {
        conn.on('notice', function (msg) {
          logger.error('Notice from PostgreSQL: ' + msg.message);
        });
        done(err, conn);
      });
    },
  },
  // Uncomment the below and 'app.useLogger(new Logger());' to the test to see Mikro-ORM logs
  // debug: ['query', 'query-params'],
});
