import { MikroOrmModule } from '@mikro-orm/nestjs';
import { Module } from '@nestjs/common';
import { ImportService } from './services/import.service';
import { QueryService } from './services/query.service';

@Module({
  imports: [MikroOrmModule.forRoot()],
  providers: [ImportService, QueryService],
  exports: [ImportService, QueryService],
})
export class DomainModule {}
