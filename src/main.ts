import { configDotenv } from 'dotenv';
configDotenv();

import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { MikroORM } from '@mikro-orm/core';
import { LogLevel } from '@nestjs/common';
import { json, urlencoded } from 'express';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Accept large payloads for event migration
  app.use(json({ limit: '50mb' }));
  app.use(urlencoded({ extended: true, limit: '50mb' }));

  app.useLogger([(process.env['LOG_LEVEL'] as LogLevel) || 'log']);

  // Run migrations if needed. Note may need to change this if multiple containers are used for scaling
  const migrator = app.get(MikroORM).getMigrator();
  await migrator.up();

  // Start the service. IP 0.0.0.0 ensure it is available to Docker
  await app.listen(5510, '0.0.0.0');
}
bootstrap();
