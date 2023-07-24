import { TsMorphMetadataProvider } from '@mikro-orm/reflection';
import { DateTimeType, Platform, TextType, Type } from '@mikro-orm/core';

class DateTimeNtzType extends DateTimeType {
  getColumnType(): string {
    return 'timestamp';
  }
}

export default {
  entities: ['./dist/domain/entities'],
  entitiesTs: ['./src/domain/entities'],
  metadataProvider: TsMorphMetadataProvider,
  dbName: 'off',
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  host: process.env.POSTGRES_HOST,
  schema: 'off',
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
};
