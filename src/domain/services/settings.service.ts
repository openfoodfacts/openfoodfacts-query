import { EntityManager } from '@mikro-orm/core';
import { Injectable } from '@nestjs/common';
import { Settings } from '../entities/settings';

@Injectable()
export class SettingsService {
  constructor(private readonly em: EntityManager) {}

  async get() {
    let settings = await this.em.findOne(Settings, 1);
    if (!settings) {
      settings = this.em.create(Settings, {});
    }
    return settings;
  }
}
