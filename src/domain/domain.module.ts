import { MikroOrmModule } from '@mikro-orm/nestjs';
import { Module } from '@nestjs/common';
import { ImportService } from './services/import.service';

@Module({
  imports: [MikroOrmModule.forRoot()],
  providers: [ImportService],
  exports: [ImportService],
})
export class DomainModule {}
