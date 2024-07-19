import { configDotenv } from 'dotenv';
configDotenv();

import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { MikroORM } from '@mikro-orm/core';
import { LogLevel } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useLogger([(process.env['LOG_LEVEL'] as LogLevel) || 'log']);

  // Run migrations if needed. Note may need to change this if multiple containers are used for scaling
  const migrator = app.get(MikroORM).getMigrator();
  await migrator.up();

  // Start the service. IP 0.0.0.0 ensure it is available to Docker
  await app.listen(5510, '0.0.0.0');
}
bootstrap();
