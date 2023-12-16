import { MikroOrmModule } from '@mikro-orm/nestjs';
import { Module } from '@nestjs/common';
import { ImportService } from './services/import.service';
import { QueryService } from './services/query.service';
import { TagService } from './services/tag.service';
import { SettingsService } from './services/settings.service';

@Module({
  imports: [MikroOrmModule.forRoot()],
  providers: [ImportService, QueryService, TagService, SettingsService],
  exports: [ImportService, QueryService, TagService, SettingsService],
})
export class DomainModule {}
