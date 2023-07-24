import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { AppController } from './app.controller';
import { MikroORM, RequestContext } from '@mikro-orm/core';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const orm = app.get(MikroORM);
  try {
    await RequestContext.createAsync(orm.em, async () => {
      //await app.get(AppController).importFromMongo();
      await app.get(AppController).importFromFile();
    });
  } finally {
    await orm.close();
  }
}
bootstrap();
