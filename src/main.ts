import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { MikroORM } from '@mikro-orm/core';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const migrator = app.get(MikroORM).getMigrator();
  await migrator.up();
  await app.listen(5510, '0.0.0.0');
}
bootstrap();
