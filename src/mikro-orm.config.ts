import { TsMorphMetadataProvider } from '@mikro-orm/reflection';
import { Platform, TextType, Type } from '@mikro-orm/core';

export default {
  entities: ['./dist/domain/entities'],
  entitiesTs: ['./src/domain/entities'],
  metadataProvider: TsMorphMetadataProvider,
  dbName: 'off',
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  schema: 'off',
  type: 'postgresql',
  discovery: {
    getMappedType(type: string, platform: Platform) {
      // override the mapping for string properties only
      if (type === 'string') {
        return Type.getType(TextType);
      }

      return platform.getDefaultMappedType(type);
    },
  },
};
