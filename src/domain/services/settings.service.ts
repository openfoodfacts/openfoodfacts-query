import { EntityManager } from '@mikro-orm/core';
import { Injectable } from '@nestjs/common';
import { Settings } from '../entities/settings';

@Injectable()
export class SettingsService {
  constructor(private readonly em: EntityManager) {}

  settings: Settings;
  async find() {
    this.settings = await this.em.findOne(Settings, 1);
    if (!this.settings) {
      this.settings = this.em.create(Settings, {});
    }
    return this.settings;
  }

  async getLastModified() {
    return (await this.find()).lastModified;
  }

  async setLastModified(lastModified: Date) {
    (await this.find()).lastModified = lastModified;
    await this.em.flush();
  }

  async getLastMessageId() {
    return (await this.find()).lastMessageId || '$';
  }

  async setLastMessageId(messageId: string) {
    (await this.find()).lastMessageId = messageId;
    await this.em.flush();
  }

  getRedisUrl() {
    return process.env.REDIS_URL;
  }
}
