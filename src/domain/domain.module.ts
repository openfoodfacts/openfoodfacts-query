import { MikroOrmModule } from '@mikro-orm/nestjs';
import { Module } from '@nestjs/common';
import { ImportService } from './services/import.service';
import { QueryService } from './services/query.service';
import { TagService } from './services/tag.service';

@Module({
  imports: [MikroOrmModule.forRoot()],
  providers: [ImportService, QueryService, TagService],
  exports: [ImportService, QueryService, TagService],
})
export class DomainModule {}
